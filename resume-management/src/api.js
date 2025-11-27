// 开发环境默认通过 Vite 代理，生产环境可以根据环境变量定制后端地址
const DEFAULT_BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'https://resume-backend.292450.xyz';
// const API_BASE_URL = 'http://127.0.0.1:5000';
const API_BASE_URL = 'https://resume-backend.292450.xyz';
/**
 * 预览简历解析结果（不保存）
 * @param {FormData} formData - 包含文件的 FormData 对象
 * @returns {Promise<Object>} 解析结果预览
 */
export async function previewResumeParse(formData) {
  const response = await fetch(`${API_BASE_URL}/preview`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '预览失败' }));
    throw new Error(error.detail || '预览失败');
  }

  return await response.json();
}

/**
 * 保存已解析的候选人信息
 * @param {Object} data - 包含解析结果和文件信息的数据
 * @returns {Promise<Object>} 保存后的候选人信息
 */
export async function saveCandidate(data) {
  const response = await fetch(`${API_BASE_URL}/save`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '保存失败' }));
    throw new Error(error.detail || '保存失败');
  }

  return await response.json();
}

/**
 * 上传简历文件（直接保存，保留兼容性）
 * @param {FormData} formData - 包含文件的 FormData 对象
 * @returns {Promise<Object>} 解析后的候选人信息
 */
export async function uploadResume(formData) {
  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '上传失败' }));
    throw new Error(error.detail || '上传失败');
  }

  return await response.json();
}

/**
 * 获取候选人列表
 * @param {string} tag - 可选的标签筛选参数
 * @param {string} name - 可选的姓名模糊搜索参数
 * @param {string} degree - 可选的学历筛选参数
 * @param {number} page - 页码，从1开始
 * @param {number} pageSize - 每页数量
 * @returns {Promise<Object>} 分页结果 { total, page, page_size, total_pages, data }
 */
export async function fetchCandidates(tag = null, name = null, degree = null, page = 1, pageSize = 10) {
  const params = new URLSearchParams();
  if (tag) {
    params.append('tag', tag);
  }
  if (name) {
    params.append('name', name);
  }
  if (degree) {
    params.append('degree', degree);
  }
  params.append('page', page.toString());
  params.append('page_size', pageSize.toString());

  const url = `${API_BASE_URL}/candidates?${params.toString()}`;
  const response = await fetch(url);

  if (!response.ok) {
    if (response.status === 401) {
      window.location.href = '/login';
      return;
    }
    throw new Error('获取候选人列表失败');
  }

  return await response.json();
}

/**
 * 更新候选人标签
 * @param {number} candidateId - 候选人ID
 * @param {string} tags - 标签字符串，多个标签用逗号分隔
 * @returns {Promise<Object>} 更新后的候选人信息
 */
export async function updateCandidateTags(candidateId, tags) {
  const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/tags`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ tags }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '更新标签失败' }));
    throw new Error(error.detail || '更新标签失败');
  }

  return await response.json();
}

/**
 * 更新候选人备注
 * @param {number} candidateId - 候选人ID
 * @param {string} notes - 备注内容
 * @returns {Promise<Object>} 更新后的候选人信息
 */
export async function updateCandidateNotes(candidateId, notes) {
  const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/notes`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ notes }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '更新备注失败' }));
    throw new Error(error.detail || '更新备注失败');
  }

  return await response.json();
}

/**
 * 获取所有标签列表
 * @returns {Promise<Array>} 标签列表
 */
export async function fetchAllTags() {
  const response = await fetch(`${API_BASE_URL}/tags`);

  if (!response.ok) {
    throw new Error('获取标签列表失败');
  }

  return await response.json();
}

/**
 * 下载简历文件
 * @param {number} candidateId - 候选人ID
 */
export function downloadResume(candidateId) {
  const url = `${API_BASE_URL}/candidates/${candidateId}/resume/download`;
  window.open(url, '_blank');
}

/**
 * 获取 DOCX 文件的 HTML 预览内容
 * @param {number} candidateId - 候选人ID
 * @returns {Promise<Object>} HTML 预览内容
 */
export async function getDocxHtmlPreview(candidateId) {
  const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}/resume/preview-html`);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '获取预览失败' }));
    throw new Error(error.detail || '获取预览失败');
  }

  return await response.json();
}

/**
 * 删除候选人
 * @param {number} candidateId - 候选人ID
 * @returns {Promise<Object>} 删除结果
 */
export async function deleteCandidate(candidateId) {
  const response = await fetch(`${API_BASE_URL}/candidates/${candidateId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '删除失败' }));
    throw new Error(error.detail || '删除失败');
  }

  return await response.json();
}
