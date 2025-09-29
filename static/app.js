function updateAuthUI() {
    const elUser = document.getElementById('authUser');
    const btnLogin = document.getElementById('btnLogin');
    const btnRegister = document.getElementById('btnRegister');
    const btnLogout = document.getElementById('btnLogout');
    const adminLinks = document.getElementById('adminLinks');
    if (store.user) {
        elUser.textContent = `${store.user.email} (${store.user.role || 'USER'})`;
        btnLogin.classList.add('hidden');
        btnRegister.classList.add('hidden');
        btnLogout.classList.remove('hidden');
        adminLinks.classList.toggle('hidden', (store.user.role !== 'ADMIN'));
    } else {
        elUser.textContent = '';
        btnLogin.classList.remove('hidden');
        btnRegister.classList.remove('hidden');
        btnLogout.classList.add('hidden');
        adminLinks.classList.add('hidden');
    }
}

const views = {
    async home() {
        const posts = await listPosts().catch(e => ({error: e.message}));
        if (posts?.error) {
            return `<div class="card">
        <h2>Посты</h2>
        <p class="error">Не удалось загрузить посты. ${posts.error}</p>
        <p><small>Если API закрыто, войдите или зарегистрируйтесь.</small></p>
      </div>`;
        }
        return `<div>
      <div class="card"><h2>Посты</h2></div>
      <div class="grid">
        ${posts.map(p => `
          <div class="card">
            <h3>${escapeHtml(p.title)}</h3>
            <p class="muted">Категория: <span class="badge">${escapeHtml(p.category?.title || '—')}</span></p>
            <div class="actions">
              <a href="#/posts/${p.id}" class="btn">Читать</a>
            </div>
          </div>
        `).join('')}
      </div>
    </div>`;
    },
    async categories() {
        try {
            const cats = await listCategories();
            return `<div>
        <div class="card"><h2>Категории</h2></div>
        <div class="grid">
          ${cats.map(c => `
            <div class="card">
              <h3>${escapeHtml(c.title)}</h3>
              <p>${escapeHtml(c.description || '')}</p>
              <a href="#/categories/${c.id}" class="btn muted">Детали</a>
            </div>
          `).join('')}
        </div>
      </div>`;
        } catch (e) {
            return `<div class="card">
        <h2>Категории</h2>
        <p class="error">Ошибка загрузки категорий: ${e.message}</p>
      </div>`;
        }
    },
    async categoryDetail(id) {
        try {
            const cat = await readCategory(id);
            const posts = await listPostsWithCategory(id);

            return `<div class="card">
              <h3>${escapeHtml(cat.title)}</h3>
              <p>${escapeHtml(cat.description || '')}</p>
            </div>
            <div class="grid">
            ${posts.map(p => `
              <div class="card">
                <h3>${escapeHtml(p.title)}</h3>
                <p class="muted">Категория: <span class="badge">${escapeHtml(cat.title)}</span></p>
                <div class="actions">
                  <a href="#/posts/${p.id}" class="btn">Читать</a>
                </div>
              </div>
            `).join('')}
            </div>`;
        } catch (e) {
            return `<div class="card"><p class="error">Ошибка: ${e.message}</p></div>`;
        }
    },
    async postDetail(id) {
        try {
            const p = await readPost(id);
            return `<article class="card">
        <h2>${escapeHtml(p.title)}</h2>
        <p class="muted"><span class="badge">${escapeHtml(p.category?.title || '—')}</span></p>
        <div>${sanitizeHtml(p.body || p.content_html || '')}</div>
      </article>`;
        } catch (e) {
            return `<div class="card"><p class="error">Ошибка: ${e.message}</p></div>`;
        }
    },
    async adminPosts() {
        const posts = await adminListPosts().catch(e => ({error: e.message}));
        if (posts.error) {
            return `<div class="card"><p class="error">${posts.error}</p></div>`;
        }
        return `<div>
      <div class="card actions">
        <button data-action="admin-create-post">Создать пост</button>
      </div>
      <table class="table card">
        <thead><tr><th>ID</th><th>Заголовок</th><th>Текст</th><th></th></tr></thead>
        <tbody>
          ${posts.map(p => `
            <tr>
              <td>${p.id}</td>
              <td>${escapeHtml(p.title)}</td>
              <td>${escapeHtml(p.body.substring(0, 10) + (p.body.length > 10 ? '...' : ''))}</td>
              <td class="actions">
                <a href="#/admin/posts/${p.id}">Править</a>
                <button data-action="admin-delete-post" data-id="${p.id}" class="danger">Удалить</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>`;
    },
    async adminPostEdit(id) {
        const cats = await adminListCategories().catch(() => []);
        const post = id ? await adminGetPost(id) : {id: null, title: '', body: '', category: null};
        return `<div class="card">
      <h2>${id ? 'Редактирование' : 'Создание'} поста</h2>
      <form id="formPost" data-id="${id || ''}">
        <label>Заголовок <input name="title" required value="${escapeAttr(post.title || '')}"/></label>
        <label>Текст (HTML) <textarea name="body" rows="8">${escapeHtml(post.body || '')}</textarea></label>
        <label>Категория
          <select name="categoryId" required>
            ${cats.map(c => `<option value="${c.id}" ${post.category?.id === c.id ? 'selected' : ''}>${escapeHtml(c.title)}</option>`).join('')}
          </select>
        </label>
        <div class="actions">
          <button type="submit">${id ? 'Сохранить' : 'Создать'}</button>
          <a href="#/admin/posts">Назад</a>
        </div>
      </form>
    </div>`;
    },
    async adminCategories() {
        const cats = await adminListCategories().catch(e => ({error: e.message}));
        if (cats.error) {
            return `<div class="card"><p class="error">${cats.error}</p></div>`;
        }
        return `<div>
      <div class="card actions">
        <button data-action="admin-create-category">Создать категорию</button>
      </div>
      <table class="table card">
        <thead><tr><th>ID</th><th>Название</th><th>Описание</th><th></th></tr></thead>
        <tbody>
          ${cats.map(c => `
            <tr>
              <td>${c.id}</td>
              <td>${escapeHtml(c.title)}</td>
              <td><small>${escapeHtml(c.description || '')}</small></td>
              <td class="actions">
                <a href="#/admin/categories/${c.id}">Править</a>
                <button data-action="admin-delete-category" data-id="${c.id}" class="danger">Удалить</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>`;
    },
    async adminCategoryEdit(id) {
        const cat = id ? await adminGetCategory(id) : {id: null, title: '', description: ''};
        return `<div class="card">
      <h2>${id ? 'Редактирование' : 'Создание'} категории</h2>
      <form id="formCategory" data-id="${id || ''}">
        <label>Название <input name="title" required value="${escapeAttr(cat.title || '')}"/></label>
        <label>Описание <textarea name="description" rows="5">${escapeHtml(cat.description || '')}</textarea></label>
        <div class="actions">
          <button type="submit">${id ? 'Сохранить' : 'Создать'}</button>
          <a href="#/admin/categories">Назад</a>
        </div>
      </form>
    </div>`;
    },
    async adminUsers() {
        const users = await adminListUsers().catch(e => ({error: e.message}));
        if (users.error) {
            return `<div class="card"><p class="error">${users.error}</p></div>`;
        }
        return `<div>
      <table class="table card">
        <thead><tr><th>ID</th><th>Email</th><th>Роль</th><th>Активен</th><th></th></tr></thead>
        <tbody>
          ${users.map(u => `
            <tr>
              <td>${u.id}</td>
              <td>${escapeHtml(u.email)}</td>
              <td>${u.role}</td>
              <td>${u.isActive ? 'да' : 'нет'}</td>
              <td class="actions">
                <button data-action="admin-restrict-user" data-id="${u.id}">Сделать USER</button>
                <button data-action="admin-promote-user" data-id="${u.id}">Сделать ADMIN</button>
                <button data-action="admin-delete-user" data-id="${u.id}" class="danger">Удалить</button>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    </div>`;
    }
};

route('/', views.home);
route('/categories', views.categories);
route('/admin/posts', views.adminPosts);
route('/admin/categories', views.adminCategories);
route('/admin/users', views.adminUsers);

document.getElementById('btnLogin').addEventListener('click', () => document.getElementById('dlgLogin').showModal());
document.getElementById('btnRegister').addEventListener('click', () => document.getElementById('dlgRegister').showModal());
document.getElementById('btnLogout').addEventListener('click', () => {
    clearAuth();
    navigate('#/');
});
document.getElementById('cancelLogin').addEventListener('click', () => document.getElementById('dlgLogin').close());
document.getElementById('cancelRegister').addEventListener('click', () => document.getElementById('dlgRegister').close());

document.getElementById('formLogin').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const email = fd.get('email');
    const password = fd.get('password');
    try {
        await loginUser(email, password);
        document.getElementById('dlgLogin').close();
        location.hash = '#/';
    } catch (err) {
        document.getElementById('loginError').textContent = 'Ошибка: ' + err.message;
    }
});

document.getElementById('formRegister').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(e.target);
    const email = fd.get('email');
    const password = fd.get('password');
    try {
        await registerUser(email, password);
        document.getElementById('dlgRegister').close();
        location.hash = '#/';
    } catch (err) {
        document.getElementById('registerError').textContent = 'Ошибка: ' + err.message;
    }
});

function attachActions() {
    document.querySelectorAll('[data-action="admin-delete-post"]').forEach(btn => {
        btn.onclick = async () => {
            if (confirm('Удалить пост?')) {
                await adminDeletePost(btn.dataset.id);
                location.hash = '#/admin/posts';
                location.reload();
            }
        };
    });
    document.querySelectorAll('[data-action="admin-delete-category"]').forEach(btn => {
        btn.onclick = async () => {
            if (confirm('Удалить категорию?')) {
                await adminDeleteCategory(btn.dataset.id);
                location.hash = '#/admin/categories';
                location.reload();
            }
        };
    });
    document.querySelectorAll('[data-action="admin-promote-user"]').forEach(btn => {
        btn.onclick = async () => {
            await adminUpdateUser(btn.dataset.id, 'ADMIN');
            alert('Роль обновлена');
            location.reload();
        };
    });
    document.querySelectorAll('[data-action="admin-restrict-user"]').forEach(btn => {
        btn.onclick = async () => {
            await adminUpdateUser(btn.dataset.id, 'USER');
            alert('Роль обновлена');
            location.reload();
        };
    });
    document.querySelectorAll('[data-action="admin-delete-user"]').forEach(btn => {
        btn.onclick = async () => {
            await adminDeleteUser(btn.dataset.id);
            location.reload();
        };
    });
    document.querySelectorAll('[data-action="admin-create-post"]').forEach(btn => {
        btn.onclick = () => {
            location.hash = '#/admin/posts/new';
        };
    });
    document.querySelectorAll('[data-action="admin-create-category"]').forEach(btn => {
        btn.onclick = () => {
            location.hash = '#/admin/categories/new';
        };
    });

    const formPost = document.getElementById('formPost');
    if (formPost) {
        formPost.onsubmit = async (e) => {
            e.preventDefault();
            const fd = new FormData(formPost);
            const payload = {
                title: fd.get('title'),
                body: fd.get('body'),
                category_id: Number(fd.get('categoryId'))
            };
            if (formPost.dataset.id) {
                await adminUpdatePost(formPost.dataset.id, payload);
            } else {
                await adminCreatePost(payload);
            }
            location.hash = '#/admin/posts';
        };
    }

    const formCategory = document.getElementById('formCategory');
    if (formCategory) {
        formCategory.onsubmit = async (e) => {
            e.preventDefault();
            const fd = new FormData(formCategory);
            const payload = {title: fd.get('title'), description: fd.get('description')};
            if (formCategory.dataset.id) {
                await adminUpdateCategory(formCategory.dataset.id, payload);
            } else {
                await adminCreateCategory(payload);
            }
            location.hash = '#/admin/categories';
        };
    }
}

function escapeHtml(s) {
    return (s ?? '').toString().replace(/[&<>"']/g, m => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }[m]));
}

function escapeAttr(s) {
    return escapeHtml(s).replace(/"/g, '&quot;');
}

function sanitizeHtml(html) {
    const tmp = document.createElement('div');
    tmp.innerHTML = html || '';
    const allowed = new Set(['P', 'BR', 'STRONG', 'EM', 'UL', 'OL', 'LI', 'A', 'H1', 'H2', 'H3', 'H4', 'BLOCKQUOTE', 'CODE', 'PRE']);
    [...tmp.querySelectorAll('*')].forEach(el => {
        if (!allowed.has(el.tagName)) {
            el.replaceWith(document.createTextNode(el.textContent));
        } else {
            [...el.attributes].forEach(a => {
                if (!['href', 'title', 'alt'].includes(a.name)) el.removeAttribute(a.name);
            });
        }
    });
    return tmp.innerHTML;
}

(async function boot() {
    try {
        if (!store.user) {
            await refreshToken();
        }
    } catch {
    }
    updateAuthUI();
})();
window.views = views;
