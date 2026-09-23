<template>
  <div class="panel">
    <h4>📐 ROI感兴趣区域分析</h4>
    <el-button size="small" @click="addROI" style="margin-bottom:8px">+ 添加ROI</el-button>
    <div v-for="(roi,i) in rois" :key="i" class="roi-config">
      <div class="roi-row">
        <el-checkbox v-model="roi.selected" size="small" />
        <el-input v-model="roi.label" size="small" placeholder="标签" style="width:80px"/>
        <el-input-number v-model="roi.center[0]" size="small" :min="0" :max="63" style="width:65px" controls-position="right"/>
        <el-input-number v-model="roi.center[1]" size="small" :min="0" :max="63" style="width:65px" controls-position="right"/>
        <el-input-number v-model="roi.center[2]" size="small" :min="0" :max="63" style="width:65px" controls-position="right"/>
        <el-input-number v-model="roi.radius" size="small" :min="2" :max="20" style="width:60px" controls-position="right"/>
        <el-button size="small" type="danger" @click="removeROI(i)" circle>×</el-button>
      </div>
    </div>
    <el-button type="success" size="small" @click="analyze" :loading="store.loading" :disabled="!selectedCount" style="margin-top:8px">
      📊 批量分析选中ROI ({{ selectedCount }})
    </el-button>

    <div v-if="store.roiResults.length" class="results">
      <div class="results-head">
        <span v-if="store.roiSummary" class="summary">
          共 {{ store.roiSummary.total }} 个区域：
          <b class="ok">{{ store.roiSummary.succeeded }} 成功</b>
          <template v-if="store.roiSummary.failed"> / <b class="bad">{{ store.roiSummary.failed }} 失败</b></template>
        </span>
        <el-button size="small" type="danger" plain @click="store.clearROIResults()">清除全部</el-button>
      </div>
      <table class="result-table">
        <thead>
          <tr><th>名称</th><th>均值(HU)</th><th>标准差</th><th>体素数</th><th>范围</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="(r,i) in store.roiResults" :key="i" :class="{ failed: r.status === 'error' }">
            <template v-if="r.status === 'ok'">
              <td class="c-label">{{ r.label }}</td>
              <td>{{ r.mean }}</td>
              <td>{{ r.std }}</td>
              <td>{{ r.voxelCount }}</td>
              <td>{{ r.min }}~{{ r.max }}</td>
            </template>
            <template v-else>
              <td class="c-label">{{ r.label }}</td>
              <td colspan="4" class="c-error">⚠ 测量失败：{{ r.error }}</td>
            </template>
            <td><el-button size="small" type="danger" link @click="store.removeROIResult(i)">×</el-button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useImagingStore } from '../store/imaging'
const store = useImagingStore()

interface ROIDef { label: string; center: number[]; radius: number; selected: boolean }
const rois = ref<ROIDef[]>([
  { label: 'lesion1', center: [30, 28, 32], radius: 6, selected: true }
])

const selectedCount = computed(() => rois.value.filter(r => r.selected).length)

function addROI() {
  // 默认标签自动避让已有名称，保证每个区域单独命名
  let n = rois.value.length + 1
  while (rois.value.some(r => r.label === `roi-${n}`)) n++
  rois.value.push({ label: `roi-${n}`, center: [32, 32, 32], radius: 8, selected: true })
}
function removeROI(i: number) { rois.value.splice(i, 1) }
function analyze() {
  const chosen = rois.value.filter(r => r.selected)
    .map(({ label, center, radius }) => ({ label, center: [...center], radius }))
  store.analyzeROI(chosen)
}
</script>

<style scoped>
.panel { background:#161b22; border-radius:6px; padding:10px; border:1px solid #30363d }
.panel h4 { color:#58a6ff; font-size:12px; margin-bottom:8px }
.roi-row { display:flex; gap:3px; align-items:center; padding:4px 0; font-size:11px; flex-wrap:wrap }
.results { margin-top:10px }
.results-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px }
.summary { font-size:11px; color:#8b949e }
.summary .ok { color:#3fb950 }
.summary .bad { color:#f85149 }
.result-table { width:100%; border-collapse:collapse; font-size:11px }
.result-table th { text-align:left; color:#8b949e; font-weight:500; padding:4px 6px; background:#0d1117; border-bottom:1px solid #30363d }
.result-table td { padding:4px 6px; border-bottom:1px solid #21262d; color:#e6edf3 }
.result-table tr.failed td { background:rgba(248,81,73,.06) }
.c-label { font-weight:600 }
.c-error { color:#f85149; font-size:10px }
</style>
