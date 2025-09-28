// Tiny hash router
const routes = {};

function route(path, render) {
    routes[path] = render;
}

function navigate(hash) {
    window.location.hash = hash;
}

function getPath() {
    return location.hash.replace(/^#/, '') || '/';
}

async function render() {
    const app = document.getElementById('app');
    const path = getPath();
    console.log(routes, path);

    if (routes[path]) {
        app.innerHTML = await routes[path]();
    } else if (path.startsWith('/posts/')) {
        const id = path.split('/')[2];
        app.innerHTML = await views.postDetail(id);
    }else if (path.startsWith('/categories/')) {
        const id = path.split('/')[2];
        app.innerHTML = await views.categoryDetail(id);
    } else if (path.startsWith('/admin/posts/')) {
        const seg = path.split('/')[3];
        const id = (seg && seg !== 'new' && /^\d+$/.test(seg)) ? seg : null;
        app.innerHTML = await views.adminPostEdit(id);
    } else if (path.startsWith('/admin/categories/')) {
        const seg = path.split('/')[3];
        const id = (seg && seg !== 'new' && /^\d+$/.test(seg)) ? seg : null;
        app.innerHTML = await views.adminCategoryEdit(id);
    } else {
        app.innerHTML = `<div class="card">Страница не найдена</div>`;
    }
    attachActions();
}

window.addEventListener('hashchange', render);
window.addEventListener('DOMContentLoaded', render);
