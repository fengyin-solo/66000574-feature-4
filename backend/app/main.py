import random, math
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Medical Imaging Viewer")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class VolumeRequest(BaseModel):
    preset: str = "brain"  # brain / chest / abdomen
    width: int = 64
    height: int = 64
    depth: int = 64


class ROIRequest(BaseModel):
    center: list = [32, 32, 32]
    radius: int = 10
    label: str = "lesion"


class WindowLevelRequest(BaseModel):
    window: float = 400.0
    level: float = 40.0
    preset: str = "brain"


WINDOW_PRESETS = {
    "lung":     {"window": 1500, "level": -600, "desc": "肺窗 (W1500/L-600)"},
    "mediastinum": {"window": 350, "level": 50, "desc": "纵隔窗 (W350/L50)"},
    "bone":     {"window": 2000, "level": 300, "desc": "骨窗 (W2000/L300)"},
    "brain":    {"window": 80, "level": 40, "desc": "脑窗 (W80/L40)"},
    "abdomen":  {"window": 400, "level": 40, "desc": "腹窗 (W400/L40)"},
}


def generate_volume(preset: str, w: int, h: int, d: int):
    """Generate synthetic CT-like volume"""
    np.random.seed(42)
    vol = np.zeros((d, h, w), dtype=np.float32)

    center_x, center_y, center_z = w//2, h//2, d//2
    for z in range(d):
        for y in range(h):
            for x in range(w):
                # Head-like shape
                rx = (x - center_x - 5) / (w * 0.4)
                ry = (y - center_y) / (h * 0.45)
                rz = (z - center_z + 3) / (d * 0.4)
                dist = math.sqrt(rx**2 + ry**2 + rz**2)

                if preset == "brain":
                    if dist < 0.85:
                        # Brain tissue
                        base = 35
                        # Sulci pattern
                        noise = (np.sin(x * 0.4) * np.cos(y * 0.3) + np.sin(z * 0.35)) * 8
                        # Ventricles (CSF)
                        vent_dist = math.sqrt(((x-center_x+2)/(w*0.15))**2 + ((y-center_y)/(h*0.12))**2 + ((z-center_z)/(d*0.1))**2)
                        if vent_dist < 0.6:
                            base = 10 + noise * 0.3
                        # Skull
                        if dist > 0.7 and dist < 0.85:
                            base = 200 + random.uniform(-20, 20)
                        vol[z, y, x] = base + noise
                    elif dist < 0.9:
                        vol[z, y, x] = 100  # Scalp
                elif preset == "chest":
                    # Body oval
                    bx = (x - center_x) / (w * 0.35)
                    by = (y - center_y) / (h * 0.4)
                    body = math.sqrt(bx**2 + by**2)
                    if body < 1.0:
                        # Lungs (dark)
                        lung_dist1 = math.sqrt(((x-center_x+8)/(w*0.12))**2 + ((y-center_y)/(h*0.13))**2)
                        lung_dist2 = math.sqrt(((x-center_x-8)/(w*0.12))**2 + ((y-center_y)/(h*0.13))**2)
                        if lung_dist1 < 0.7 or lung_dist2 < 0.7:
                            vol[z, y, x] = -650 + np.sin(z*0.3)*30
                        else:
                            vol[z, y, x] = 30 + np.random.uniform(-5, 5)
                        # Spine
                        if abs(x - center_x) < 3 and abs(y - center_y + 8) < 4:
                            vol[z, y, x] = 250
                    vol[z, y, x] += np.random.uniform(-3, 3)
                elif preset == "abdomen":
                    bx = (x - center_x) / (w * 0.33)
                    by = (y - center_y) / (h * 0.4)
                    body = math.sqrt(bx**2 + by**2)
                    if body < 1.0:
                        base = 35
                        # Liver (right upper)
                        lv = math.sqrt(((x-center_x-6)/(w*0.08))**2 + ((y-center_y+4)/(h*0.07))**2)
                        if lv < 0.6:
                            base = 55 + np.random.uniform(-5, 5)
                        # Kidneys
                        kd1 = math.sqrt(((x-center_x-5)/(w*0.04))**2 + ((y-center_y-5)/(h*0.04))**2)
                        kd2 = math.sqrt(((x-center_x+5)/(w*0.04))**2 + ((y-center_y-5)/(h*0.04))**2)
                        if kd1 < 0.4 or kd2 < 0.4:
                            base = 45
                        # Spine
                        if abs(x - center_x) < 3 and abs(y - center_y + 7) < 4:
                            base = 250 + np.random.uniform(-10, 10)
                        vol[z, y, x] = base + np.random.uniform(-9, 9)

    return vol.tolist()


@app.post("/api/volume")
def get_volume(req: VolumeRequest):
    vol = generate_volume(req.preset, req.width, req.height, req.depth)

    # Extract mid slices for MPR
    mid_axial = int(req.depth // 2)
    mid_coronal = int(req.height // 2)
    mid_sagittal = int(req.width // 2)

    # Return: 3D volume + 3 MPR slices
    return {
        "volume": vol,
        "dimensions": [req.depth, req.height, req.width],
        "mpr": {
            "axial": vol[mid_axial],
            "coronal": [[vol[z][mid_coronal][x] for x in range(req.width)] for z in range(req.depth)],
            "sagittal": [[vol[z][y][mid_sagittal] for y in range(req.height)] for z in range(req.depth)]
        },
        "preset": req.preset,
        "windowPresets": WINDOW_PRESETS
    }


class ROIAnalyzeRequest(BaseModel):
    volume: list
    rois: list = []


# Sphere ROIs with fewer than this many intersecting voxels cannot yield
# meaningful statistics and are reported as failed.
MIN_VOXEL_COUNT = 2


def _coerce_int(value):
    """Round numeric JSON values the same way float -> voxel index conversion did."""
    return int(round(float(value)))


def _analyze_single_roi(vol: np.ndarray, roi):
    """Measure one spherical ROI.

    Returns a dict whose success payload keeps the original measurement
    contract (mean/std/min/max/voxelCount/histogram); failures return a
    status="failed" record carrying a human-readable reason instead.
    """
    label = roi.get("label") or "roi"
    center = roi.get("center", [32, 32, 32])
    radius = roi.get("radius", 8)
    roi_id = roi.get("id")

    try:
        if not isinstance(center, (list, tuple)) or len(center) != 3 or \
                not all(isinstance(c, (int, float)) and math.isfinite(float(c)) for c in center):
            raise ValueError("中心点必须为3个数值坐标")
        cx, cy, cz = (_coerce_int(c) for c in center)
    except (TypeError, ValueError):
        return {"id": roi_id, "label": label, "center": center, "radius": radius,
                "status": "failed", "reason": "中心点无效，必须为3个数值坐标"}

    if not isinstance(radius, (int, float)) or not math.isfinite(float(radius)):
        return {"id": roi_id, "label": label, "center": list(center), "radius": radius,
                "status": "failed", "reason": "半径无效，必须为正数"}

    r = _coerce_int(radius)
    if r <= 0:
        return {"id": roi_id, "label": label, "center": list(center), "radius": radius,
                "status": "failed", "reason": "半径无效，必须为正数"}

    d, h, w = vol.shape
    if not (0 <= cx < w and 0 <= cy < h and 0 <= cz < d):
        return {"id": roi_id, "label": label, "center": [cx, cy, cz], "radius": r,
                "status": "failed",
                "reason": f"中心({cx}, {cy}, {cz})在数据范围之外，数据尺寸为({w}, {h}, {d})"}

    # Extract voxels within sphere
    voxels = []
    for z in range(max(0, cz-r), min(d, cz+r+1)):
        for y in range(max(0, cy-r), min(h, cy+r+1)):
            for x in range(max(0, cx-r), min(w, cx+r+1)):
                if math.sqrt((x-cx)**2 + (y-cy)**2 + (z-cz)**2) <= r:
                    voxels.append(float(vol[z, y, x]))

    if len(voxels) == 0:
        return {"id": roi_id, "label": label, "center": [cx, cy, cz], "radius": r,
                "status": "failed", "reason": "球体与数据无交集，未取到任何体素"}
    if len(voxels) < MIN_VOXEL_COUNT:
        return {"id": roi_id, "label": label, "center": [cx, cy, cz], "radius": r,
                "status": "failed",
                "reason": f"体素数量仅{len(voxels)}个，少于最少要求{MIN_VOXEL_COUNT}个，无法统计"}

    arr = np.array(voxels)
    return {
        "id": roi_id,
        "label": label,
        "center": [cx, cy, cz],
        "radius": r,
        "status": "ok",
        "mean": round(float(np.mean(arr)), 2),
        "std": round(float(np.std(arr)), 2),
        "min": round(float(np.min(arr)), 2),
        "max": round(float(np.max(arr)), 2),
        "voxelCount": len(voxels),
        "histogram": np.histogram(arr, bins=10, range=(float(np.min(arr)), float(np.max(arr))))[0].tolist()
    }


@app.post("/api/roi")
def analyze_roi(req: ROIAnalyzeRequest):
    try:
        vol = np.asarray(req.volume, dtype=np.float64)
        if vol.ndim != 3:
            raise ValueError("volume must be 3D")
    except Exception:
        # Volume-level failure: every requested row is marked failed.
        rows = [{
            "id": roi.get("id"), "label": roi.get("label") or "roi",
            "center": roi.get("center"), "radius": roi.get("radius"),
            "status": "failed", "reason": "体数据无法解析，请重新载入影像后再试"
        } for roi in req.rois]
        return {"rois": rows, "total": len(rows), "succeeded": 0, "failed": len(rows)}

    results = []
    for roi in req.rois:
        # A malformed ROI definition must not abort the whole batch.
        try:
            results.append(_analyze_single_roi(vol, roi))
        except Exception as exc:
            results.append({
                "id": roi.get("id"), "label": roi.get("label") or "roi",
                "center": roi.get("center"), "radius": roi.get("radius"),
                "status": "failed", "reason": f"测量异常：{exc}"
            })

    succeeded = sum(1 for r in results if r.get("status") == "ok")
    return {"rois": results, "total": len(results),
            "succeeded": succeeded, "failed": len(results) - succeeded}


@app.get("/api/windows")
def get_windows():
    return {"presets": WINDOW_PRESETS}