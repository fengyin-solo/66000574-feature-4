<template>
  <div class="panel">
    <h4>📐 ROI感兴趣区域分析</h4>

    <div class="roi-toolbar">
      <el-button size="small" @click="addROI">+ 添加ROI</el-button>
      <el-checkbox
        :model-value="allSelected"
        :indeterminate="someSelected"
        size="small"
        @change="toggleAll"
      >全选</el-checkbox>
      <span class="sel-info">已选 {{ selectedCount }}/{{ rois.length }}</span>
    </div>

    <div v-for="(roi,i) in rois" :key="roi.id" class="roi-config">
      <div class="roi-row">
        <el-checkbox v-model="roi.selected" size="small" />
        <span>ROI #{{ i+1 }}</span>
        <el-input v-model="roi.label" size="small" placeholder="名称" style="width:80px"/>
        <el-input-number v-model="roi.center[0]" size="small" :min="0" :max="80" style="width:65px" controls-position="right"/>
        <el-input-number v-model="roi.center[1]" size="small" :min="0" :max="80" style="width:65px" controls-position="right"/>
        <el-input-number v-model="roi.center[2]" size="small" :min="0" :max="80" style="width:65px" controls-position="right"/>
        <el-input-number v-model="roi.radius" size="small" :min="2" :max="20" style="width:60px" controls-position="right"/>
        <el-button size="small" type="danger" @click="removeROI(i)" circle>×</el-button>
      </div>
    </div>

    <el-button
      type="success"
      size="small"
      @click="analyze"
      :loading="store.loading"
      :disabled="!selectedCount"
      style="margin-top:8px"
    >📊 批量分析选中区域 ({{ selectedCount }})</el-button>

    <div v-if="store.roiResults.length" class="results">
      <div class="results-head">
        <span class="results-title">测量结果汇总</span>
        <span class="results-summary" v-if="store.roiSummary">
          共 {{ store.roiSummary.total }} 条 ·
          成功 <b class="ok-text">{{ store.roiSummary.succeeded }}</b> ·
          失败 <b :class="store.roiSummary.failed ? 'fail-text' : ''">{{ store.roiSummary.failed }}</b>
        </span>
        <el-button size="small" type="danger" plain @click="store.clearROIResults()">整组清除</el-button>
      </div>

      <div class="result-table">
        <div class="rt-head rt-row">
          <span class="c-idx">#</span>
          <span class="c-name">名称</span>
          <span class="c-num">均值(HU)</span>
          <span class="c-num">标准差</span>
          <span class="c-num">体素数</span>
          <span class="c-range">范围</span>
          <span class="c-act"></span>
        </div>
        <div
          v-for="(r,i) in store.roiResults"
          :key="i"
          class="rt-row rt-body"
          :class="{ 'is-failed': r.status === 'failed' }"
        >
          <span class="c-idx">{{ i+1 }}</span>
          <span class="c-name">
            <span :class="r.status === 'ok' ? 'status-dot ok' : 'status-dot fail'"></span>
            {{ r.label || '（未命名）' }}
            <div v-if="r.status === 'failed'" class="reason">⚠ {{ r.reason }}</div>
          </span>
          <template v-if="r.status === 'ok'">
            <span class="c-num">{{ fmt(r.mean) }}</span>
            <span class="c-num">{{ fmt(r.std) }}</span>
            <span class="c-num">{{ r.voxelCount }}</span>
            <span class="c-range">{{ r.min }} ~ {{ r.max }}</span>
          </template>
          <span v-else class="c-failed" colspan="4">测量失败</span>
          <span class="c-act">
            <el-button size="small" text type="danger" @click="store.removeROIResult(i)">移除</el-button>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useImagingStore } from '../store/imaging'
const store = useImagingStore()

let roiSeq = 0
interface ROIDef { id: number; label: string; center: number[]; radius: number; selected: boolean }
const rois = ref<ROIDef[]>([
  { id: ++roiSeq, label: 'lesion1', center: [30, 28, 32], radius: 6, selected: true }
])

function addROI() {
  rois.value.push({
    id: ++roiSeq,
    label: `roi-${rois.value.length + 1}`,
    center: [32, 32, 32], radius: 8, selected: true
  })
}
function removeROI(i: number) { rois.value.splice(i, 1) }

const selectedCount = computed(() => rois.value.filter(r => r.selected).length)
const allSelected = computed(() => rois.value.length > 0 && selectedCount.value === rois.value.length)
const someSelected = computed(() => selectedCount.value > 0 && selectedCount.value < rois.value.length)
function toggleAll(val: any) {
  rois.value.forEach(r => { r.selected = Boolean(val) })
}

async function analyze() {
  const picked = rois.value.filter(r => r.selected)
  if (!picked.length) return
  try {
    await store.analyzeROI(picked.map(r => ({
      id: r.id, label: r.label, center: [...r.center], radius: r.radius
    })))
  } catch {
    ElMessage.error('分析请求失败，请确认后端服务已启动')
  }
}

function fmt(v: number) { return Number.isFinite(v) ? v : '—' }
</script>

<style scoped>
.panel { background:#161b22; border-radius:6px; padding:10px; border:1px solid #30363d }
.panel h4 { color:#58a6ff; font-size:12px; margin-bottom:8px }
.roi-toolbar { display:flex; align-items:center; gap:8px; margin-bottom:4px }
.sel-info { font-size:10px; color:#8b949e; margin-left:auto }
.roi-row { display:flex; gap:3px; align-items:center; padding:4px 0; font-size:11px; flex-wrap:wrap }

.results { margin-top:10px }
.results-head { display:flex; align-items:center; gap:8px; margin-bottom:6px }
.results-title { font-size:12px; color:#e6edf3; font-weight:600 }
.results-summary { font-size:10px; color:#8b949e; margin-left:auto }
.ok-text { color:#3fb950 }
.fail-text { color:#f85149 }

.result-table { border:1px solid #30363d; border-radius:4px; overflow:hidden }
.rt-row { display:grid; grid-template-columns:26px 1.4fr 0.8fr 0.7fr 0.6fr 1.1fr 40px; align-items:center; font-size:10px }
.rt-head { background:#0d1117; color:#8b949e; padding:4px 6px }
.rt-body { padding:5px 6px; border-top:1px solid #21262d; background:#161b22 }
.rt-body.is-failed { background:rgba(248,81,73,0.08) }
.c-idx { color:#8b949e }
.c-name { color:#e6edf3; word-break:break-all; display:flex; align-items:center; gap:4px; flex-wrap:wrap }
.c-num, .c-range { color:#c9d1d9; font-family:monospace }
.c-act { text-align:right }
.c-failed { color:#f85149; font-size:10px; grid-column:span 4 }
.status-dot { width:6px; height:6px; border-radius:50%; display:inline-block; flex:none }
.status-dot.ok { background:#3fb950 }
.status-dot.fail { background:#f85149 }
.reason { flex-basis:100%; color:#f85149; font-size:10px; line-height:1.4 }
</style>
