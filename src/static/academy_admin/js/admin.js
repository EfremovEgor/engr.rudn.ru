/* Медиатека в админке: копирование ссылок, загрузка файлов, вставка в редактор. */
(function () {
  "use strict";

  const PICKER_URL = "/_media-library/picker/";

  function csrfToken() {
    const input = document.querySelector("input[name=csrfmiddlewaretoken]");
    if (input) return input.value;
    const match = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  function toast(text) {
    const el = document.createElement("div");
    el.textContent = text;
    el.style.cssText =
      "position:fixed;bottom:24px;right:24px;z-index:2000;background:#111827;color:#fff;padding:10px 16px;border-radius:8px;font-size:14px;box-shadow:0 6px 20px rgb(0 0 0/.2)";
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 2200);
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
  }

  function absoluteUrl(url) {
    try {
      return new URL(url, window.location.origin).href;
    } catch (e) {
      return url;
    }
  }

  /* ---------- Копирование ссылок ---------- */
  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-copy]");
    if (!button) return;
    event.preventDefault();
    const url = absoluteUrl(button.dataset.copy);
    navigator.clipboard.writeText(url).then(
      () => toast("Ссылка скопирована"),
      () => window.prompt("Скопируйте ссылку:", url)
    );
  });

  /* ---------- Страница массовой загрузки ---------- */
  function initDropzone() {
    const zone = document.getElementById("media-dropzone");
    if (!zone) return;
    const input = document.getElementById("media-input");
    const list = document.getElementById("media-upload-list");
    const folder = document.getElementById("media-folder");

    function uploadOne(file) {
      const row = document.createElement("div");
      row.className = "media-upload-item";
      row.innerHTML = `<span style="min-width:220px">${escapeHtml(file.name)}</span><progress max="100" value="0"></progress><span class="status academy-muted">…</span>`;
      list.prepend(row);
      const progress = row.querySelector("progress");
      const status = row.querySelector(".status");
      const data = new FormData();
      data.append("file", file);
      if (folder && folder.value) data.append("folder", folder.value);
      const xhr = new XMLHttpRequest();
      xhr.open("POST", zone.dataset.uploadUrl);
      xhr.setRequestHeader("X-CSRFToken", csrfToken());
      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) progress.value = Math.round((e.loaded / e.total) * 100);
      };
      xhr.onload = () => {
        let payload = {};
        try {
          payload = JSON.parse(xhr.responseText);
        } catch (e) {}
        if (xhr.status === 200) {
          progress.value = 100;
          status.innerHTML = `<a href="${escapeHtml(payload.url)}" target="_blank">готово</a> <button type="button" class="media-copy" data-copy="${escapeHtml(payload.url)}" title="Скопировать ссылку"><span class="material-symbols-outlined">content_copy</span></button>`;
        } else {
          status.textContent = (payload.error && payload.error.message) || "Ошибка загрузки";
          status.style.color = "#b91c1c";
        }
      };
      xhr.onerror = () => {
        status.textContent = "Ошибка сети";
        status.style.color = "#b91c1c";
      };
      xhr.send(data);
    }

    zone.addEventListener("click", () => input.click());
    input.addEventListener("change", () => Array.from(input.files).forEach(uploadOne));
    ["dragenter", "dragover"].forEach((name) =>
      zone.addEventListener(name, (e) => {
        e.preventDefault();
        zone.classList.add("is-over");
      })
    );
    ["dragleave", "drop"].forEach((name) =>
      zone.addEventListener(name, (e) => {
        e.preventDefault();
        zone.classList.remove("is-over");
      })
    );
    zone.addEventListener("drop", (e) => Array.from(e.dataTransfer.files).forEach(uploadOne));
  }

  /* ---------- Окно выбора файла из медиатеки ---------- */
  function openPicker(onSelect) {
    const modal = document.createElement("div");
    modal.className = "media-modal";
    modal.innerHTML = `
      <div class="media-modal__box" role="dialog" aria-label="Медиатека">
        <div class="media-modal__head">
          <input type="search" placeholder="Поиск по названию или имени файла">
          <select>
            <option value="">Все типы</option>
            <option value="image">Изображения</option>
            <option value="document">Документы</option>
            <option value="video">Видео</option>
            <option value="archive">Архивы</option>
          </select>
          <button type="button" class="academy-action" data-close>Закрыть</button>
        </div>
        <div class="media-modal__grid"></div>
        <div class="media-modal__foot">
          <span class="academy-muted" data-total></span>
          <span><button type="button" data-prev>←</button> <span data-page></span> <button type="button" data-next>→</button></span>
        </div>
      </div>`;
    document.body.appendChild(modal);
    const grid = modal.querySelector(".media-modal__grid");
    const search = modal.querySelector("input");
    const kind = modal.querySelector("select");
    let page = 1;
    let pages = 1;
    let timer = null;

    function close() {
      modal.remove();
      document.removeEventListener("keydown", onKey);
    }
    function onKey(e) {
      if (e.key === "Escape") close();
    }
    document.addEventListener("keydown", onKey);

    function load() {
      const params = new URLSearchParams({ q: search.value, kind: kind.value, page: page });
      grid.innerHTML = '<span class="academy-muted">Загрузка…</span>';
      fetch(`${PICKER_URL}?${params}`, { credentials: "same-origin" })
        .then((r) => r.json())
        .then((data) => {
          pages = data.pages || 1;
          modal.querySelector("[data-page]").textContent = `${data.page} / ${pages}`;
          modal.querySelector("[data-total]").textContent = `Найдено файлов: ${data.total}`;
          if (!data.items.length) {
            grid.innerHTML = '<span class="academy-muted">Ничего не найдено. Загрузите файл через раздел «Медиатека».</span>';
            return;
          }
          grid.innerHTML = "";
          data.items.forEach((item) => {
            const tile = document.createElement("button");
            tile.type = "button";
            tile.className = "media-tile";
            const thumb = item.is_image
              ? `<img src="${escapeHtml(item.url)}" alt="">`
              : `<span class="material-symbols-outlined">description</span>`;
            tile.innerHTML = `<div class="media-tile__thumb">${thumb}</div><div class="media-tile__name" title="${escapeHtml(item.title)}">${escapeHtml(item.title)}</div>`;
            tile.addEventListener("click", () => {
              onSelect(item);
              close();
            });
            grid.appendChild(tile);
          });
        })
        .catch(() => {
          grid.innerHTML = '<span class="academy-muted">Не удалось загрузить список файлов.</span>';
        });
    }

    search.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        page = 1;
        load();
      }, 300);
    });
    kind.addEventListener("change", () => {
      page = 1;
      load();
    });
    modal.querySelector("[data-prev]").addEventListener("click", () => {
      if (page > 1) {
        page -= 1;
        load();
      }
    });
    modal.querySelector("[data-next]").addEventListener("click", () => {
      if (page < pages) {
        page += 1;
        load();
      }
    });
    modal.querySelector("[data-close]").addEventListener("click", close);
    modal.addEventListener("click", (e) => {
      if (e.target === modal) close();
    });
    load();
    search.focus();
  }

  function insertIntoEditor(editor, item) {
    if (item.is_image) {
      editor.execute("insertImage", { source: [{ src: item.url, alt: item.alt || "" }] });
      return;
    }
    editor.model.change((writer) => {
      const text = writer.createText(item.title, { linkHref: item.url });
      editor.model.insertContent(text, editor.model.document.selection);
    });
  }

  function attachPickerButtons(root) {
    (root || document).querySelectorAll("textarea.django_ckeditor_5").forEach((textarea) => {
      if (textarea.id.includes("__prefix__") || textarea.dataset.mediaButton) return;
      textarea.dataset.mediaButton = "1";
      const container = textarea.closest(".ck-editor-container") || textarea.parentElement;
      const button = document.createElement("button");
      button.type = "button";
      button.className = "academy-action media-picker-btn";
      button.innerHTML = '<span class="material-symbols-outlined">perm_media</span>Медиатека: вставить файл или изображение';
      button.addEventListener("click", () => {
        const editor = window.editors && window.editors[textarea.id];
        if (!editor) {
          toast("Редактор ещё загружается");
          return;
        }
        openPicker((item) => insertIntoEditor(editor, item));
      });
      container.appendChild(button);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    initDropzone();
    attachPickerButtons();
    new MutationObserver((mutations) => {
      mutations.forEach((m) =>
        m.addedNodes.forEach((node) => {
          if (node.nodeType === 1) attachPickerButtons(node);
        })
      );
    }).observe(document.body, { childList: true, subtree: true });
  });
})();
