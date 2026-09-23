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


MIN_VOXELS = 8  # 有效体素数低于该值时统计不可靠，判定为"体素过少"


@app.post("/api/roi")
def analyze_roi(req: ROIAnalyzeRequest):
    """批量ROI分析：每个区域独立测量并命名，单条失败只标记该条，不影响其余区域"""
    results = []

    try:
        vol = np.array(req.volume, dtype=np.float32)
        d, h, w = vol.shape
    except Exception:
        vol = None

    for roi in req.rois:
        center = roi.get("center", [32, 32, 32])
        radius = roi.get("radius", 8)
        label = roi.get("label", "roi")
        entry = {"label": label, "center": center, "radius": radius}

        if vol is None:
            results.append({**entry, "status": "error", "error": "体数据无效"})
            continue

        # 参数校验
        try:
            cx, cy, cz = int(center[0]), int(center[1]), int(center[2])
            r = int(radius)
            if r < 0:
                raise ValueError
        except (TypeError, ValueError, IndexError):
            results.append({**entry, "status": "error", "error": "ROI参数无效"})
            continue

        # 区域完全落在数据范围之外
        if (cx + r < 0 or cx - r >= w or
                cy + r < 0 or cy - r >= h or
                cz + r < 0 or cz - r >= d):
            results.append({**entry, "status": "error",
                            "error": f"区域超出数据范围({w}×{h}×{d})"})
            continue

        # Extract voxels within sphere（测量口径与单区域原有逻辑一致）
        voxels = []
        for z in range(max(0, cz-r), min(d, cz+r+1)):
            for y in range(max(0, cy-r), min(h, cy+r+1)):
                for x in range(max(0, cx-r), min(w, cx+r+1)):
                    if math.sqrt((x-cx)**2 + (y-cy)**2 + (z-cz)**2) <= r:
                        voxels.append(float(vol[z, y, x]))

        if not voxels:
            results.append({**entry, "status": "error", "error": "区域内无有效体素"})
            continue
        if len(voxels) < MIN_VOXELS:
            results.append({**entry, "status": "error",
                            "error": f"有效体素过少({len(voxels)}<{MIN_VOXELS})"})
            continue

        arr = np.array(voxels)
        results.append({
            **entry,
            "status": "ok",
            "mean": round(float(np.mean(arr)), 2),
            "std": round(float(np.std(arr)), 2),
            "min": round(float(np.min(arr)), 2),
            "max": round(float(np.max(arr)), 2),
            "voxelCount": len(voxels),
            "histogram": np.histogram(arr, bins=10, range=(float(np.min(arr)), float(np.max(arr))))[0].tolist()
        })

    failed = sum(1 for r in results if r.get("status") == "error")
    return {
        "rois": results,
        "summary": {"total": len(results), "succeeded": len(results) - failed, "failed": failed}
    }


@app.get("/api/windows")
def get_windows():
    return {"presets": WINDOW_PRESETS}