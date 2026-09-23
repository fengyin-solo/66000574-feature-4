import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import type { VolumeData, ROIResult, ROISummary, WindowPreset } from '@/types'

export const useImagingStore = defineStore('imaging', () => {
  const loading = ref(false)
  const volumeData = ref<VolumeData | null>(null)
  const preset = ref('brain')
  const windowVal = ref(80)
  const levelVal = ref(40)
  const roiResults = ref<ROIResult[]>([])
  const roiSummary = ref<ROISummary | null>(null)
  const mprSlice = ref({ axial: 32, coronal: 32, sagittal: 32 })

  async function loadVolume() {
    loading.value = true
    try {
      const { data } = await axios.post('/api/volume', {
        preset: preset.value, width: 64, height: 64, depth: 64
      })
      volumeData.value = data
      mprSlice.value = { axial: 32, coronal: 32, sagittal: 32 }
    } finally { loading.value = false }
  }

  async function analyzeROI(rois: any[]) {
    loading.value = true
    try {
      const { data } = await axios.post('/api/roi', { volume: volumeData.value?.volume, rois })
      roiResults.value = data.rois
      roiSummary.value = data.summary ?? null
    } finally { loading.value = false }
  }

  function removeROIResult(index: number) {
    roiResults.value.splice(index, 1)
    if (roiSummary.value) {
      const failed = roiResults.value.filter(r => r.status === 'error').length
      roiSummary.value = {
        total: roiResults.value.length,
        succeeded: roiResults.value.length - failed,
        failed
      }
    }
  }

  function clearROIResults() {
    roiResults.value = []
    roiSummary.value = null
  }

  function applyWindow(w: number, l: number) { windowVal.value = w; levelVal.value = l }

  return { loading, volumeData, preset, windowVal, levelVal, roiResults, roiSummary, mprSlice,
    loadVolume, analyzeROI, removeROIResult, clearROIResults, applyWindow }
})