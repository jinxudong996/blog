import { ref } from 'vue'
import axios from 'axios'

function useURLLoader<T>(url: string) {
  const result = ref<T | null>(null)
  const loading = ref(true)
  const loaded = ref(false)
  const error = ref(null)

  axios.get(url).then((rawData) => {
    loading.value = false
    loaded.value = true
    result.value = rawData.data
    console.log("加载数据",loaded.value)
  }).catch(e => {
    error.value = e
    loading.value = false
  })
  console.log('导出前',loaded.value)
  return {
    result,
    loading,
    error,
    loaded
  }
}

export default useURLLoader