const API_BASE = localStorage.getItem('apiBase') || 'http://localhost:5000';

const store = {
  accessToken: localStorage.getItem('accessToken') || null,
  user: JSON.parse(localStorage.getItem('user') || 'null'),
};

function setAuth({ accessToken, user }){
  if(accessToken) { store.accessToken = accessToken; localStorage.setItem('accessToken', accessToken); }
  if(user) { store.user = user; localStorage.setItem('user', JSON.stringify(user)); }
  updateAuthUI();
}

function clearAuth(){
  store.accessToken = null;
  store.user = null;
  localStorage.removeItem('accessToken');
  localStorage.removeItem('user');
  updateAuthUI();
}

async function http(path, { method='GET', body, auth=true } = {}){
  const headers = { 'Content-Type':'application/json' };
  if(auth && store.accessToken){
    headers['Authorization'] = `Bearer ${store.accessToken}`;
  }
  const res = await fetch(API_BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    credentials: 'include',
  });
  if(res.status === 401 && auth){
    try{
      const refreshed = await refreshToken();
      if(refreshed){
        return await http(path, { method, body, auth });
      }
    }catch{}
  }
  if(!res.ok){
    const text = await res.text().catch(()=>'');
    throw new Error(text || res.statusText);
  }
  const ct = res.headers.get('content-type') || '';
  if(ct.includes('application/json')) return res.json();
  return res.text();
}

// Auth
async function registerUser(email, password){ const data = await http('/api/v1/auth/register', { method:'POST', body:{ email, password }, auth:false }); setAuth(data); return data; }
async function loginUser(email, password){ const data = await http('/api/v1/auth/login', { method:'POST', body:{ email, password }, auth:false }); setAuth(data); return data; }
async function refreshToken(){ try{ const data = await http('/api/v1/auth/refresh', { method:'POST', auth:false }); setAuth(data); return true; }catch(e){ clearAuth(); return false; } }
async function getMe(){ return http('/api/v1/users/me'); }

// Users (admin)
async function adminListUsers(page=0, pageSize=50){ return http(`/api/v1/users/admin/?page=${page}&page_size=${pageSize}`); }
async function adminGetUser(id){ return http(`/api/v1/users/admin/${id}`); }
async function adminUpdateUser(id, role){ return http(`/api/v1/users/admin/${id}`, { method:'PUT', body:{ role }}); }
async function adminDeleteUser(id){ return http(`/api/v1/users/admin/${id}`, { method:'DELETE' }); }

// Posts
async function listPosts(){ return http('/api/v1/posts/'); }
async function readPost(id){ return http(`/api/v1/posts/${id}`); }

// Admin posts
async function adminListPosts(){ return http('/api/v1/admin/posts/'); }
async function adminCreatePost(payload){ return http('/api/v1/admin/posts/', { method:'POST', body:payload }); }
async function adminGetPost(id){ return http(`/api/v1/admin/posts/${id}`); }
async function adminUpdatePost(id, payload){ return http(`/api/v1/admin/posts/${id}`, { method:'PUT', body:payload }); }
async function adminDeletePost(id){ return http(`/api/v1/admin/posts/${id}`, { method:'DELETE' }); }

// Categories
async function listCategories(){ return http('/api/v1/categories/'); }
async function readCategory(id){ return http(`/api/v1/categories/${id}`); }

// Admin categories
async function adminListCategories(){ return http('/api/v1/admin/categories/'); }
async function adminCreateCategory(payload){ return http('/api/v1/admin/categories/', { method:'POST', body:payload }); }
async function adminGetCategory(id){ return http(`/api/v1/admin/categories/${id}`); }
async function adminUpdateCategory(id, payload){ return http(`/api/v1/admin/categories/${id}`, { method:'PUT', body:payload }); }
async function adminDeleteCategory(id){ return http(`/api/v1/admin/categories/${id}`, { method:'DELETE' }); }
