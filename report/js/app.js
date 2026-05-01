const STATUS_META = {
    supported: {
        label: "supported",
        classes: "border-support-border bg-support-bg/50 text-support-fg dark:border-emerald-400/40 dark:bg-emerald-500/15 dark:text-emerald-200"
    },
    disabled: {
        label: "disabled",
        classes: "border-disabled-border bg-disabled-bg/50 text-disabled-fg dark:border-amber-300/40 dark:bg-amber-500/15 dark:text-amber-200"
    },
    unsupported: {
        label: "unsupported",
        classes: "border-unsupported-border bg-unsupported-bg/50 text-unsupported-fg dark:border-rose-300/40 dark:bg-rose-500/15 dark:text-rose-200"
    },
    unknown: {
        label: "unknown",
        classes: "border-unknown-border bg-unknown-bg/50 text-unknown-fg dark:border-slate-400/40 dark:bg-slate-500/15 dark:text-slate-200"
    }
};

const URLS = {
    readme: "https://github.com/Endkind/papermc/blob/main/versions/{version}/README.md",
    issues: "https://github.com/Endkind/papermc/issues"
};

const STORAGE_KEYS = {
    theme: "theme"
};

const tableBody = document.getElementById("version-table");
const loadState = document.getElementById("load-state");
const themeToggle = document.getElementById("theme-toggle");
const themeIcon = document.getElementById("theme-icon");
const scrollTopButton = document.getElementById("scroll-top");
const versionsTable = document.getElementById("versions-table");

let versionsDataTable = null;

function getStoredTheme() {
    try {
        const value = localStorage.getItem(STORAGE_KEYS.theme);
        if (value === "dark" || value === "light") {
            return value;
        }
    } catch (error) {
        return null;
    }

    return null;
}

function getSystemTheme() {
    if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
        return "dark";
    }

    return "light";
}

function applyTheme(theme) {
    const isDark = theme === "dark";
    document.documentElement.classList.toggle("dark", isDark);

    if (themeToggle) {
        themeToggle.setAttribute("aria-label", isDark ? "Current theme: dark" : "Current theme: light");
        themeToggle.setAttribute("title", isDark ? "Current theme: dark" : "Current theme: light");
    }
}

function updateThemeControlState(theme, isSystem) {
    if (!themeIcon) {
        return;
    }

    if (isSystem) {
        themeIcon.className = "bi bi-circle-half";
        if (themeToggle) {
            themeToggle.setAttribute("aria-label", "Current theme: system");
            themeToggle.setAttribute("title", "Current theme: system");
        }
        return;
    }

    if (theme === "dark") {
        themeIcon.className = "bi bi-moon-fill";
        return;
    }

    themeIcon.className = "bi bi-sun-fill";
}

function persistTheme(theme) {
    try {
        localStorage.setItem(STORAGE_KEYS.theme, theme);
    } catch (error) {
        return;
    }
}

function setupTheme() {
    const storedTheme = getStoredTheme();
    const initialTheme = storedTheme || getSystemTheme();
    applyTheme(initialTheme);
    updateThemeControlState(initialTheme, !storedTheme);

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const nextTheme = document.documentElement.classList.contains("dark") ? "light" : "dark";
            applyTheme(nextTheme);
            persistTheme(nextTheme);
            updateThemeControlState(nextTheme, false);
        });
    }

    if (typeof window.matchMedia === "function") {
        const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
        if (mediaQuery && typeof mediaQuery.addEventListener === "function") {
            mediaQuery.addEventListener("change", (event) => {
                if (!getStoredTheme()) {
                    const nextSystemTheme = event.matches ? "dark" : "light";
                    applyTheme(nextSystemTheme);
                    updateThemeControlState(nextSystemTheme, true);
                }
            });
        }
    }
}

function setupScrollTopButton() {
    if (!scrollTopButton) {
        return;
    }

    const updateVisibility = () => {
        const shouldShow = window.scrollY > 280;
        scrollTopButton.classList.toggle("opacity-0", !shouldShow);
        scrollTopButton.classList.toggle("pointer-events-none", !shouldShow);

        if (shouldShow) {
            scrollTopButton.removeAttribute("aria-hidden");
            scrollTopButton.removeAttribute("tabindex");
        } else {
            scrollTopButton.setAttribute("aria-hidden", "true");
            scrollTopButton.setAttribute("tabindex", "-1");
        }
    };

    scrollTopButton.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    });

    scrollTopButton.classList.add("transition", "duration-200", "opacity-0", "pointer-events-none");
    window.addEventListener("scroll", updateVisibility, { passive: true });
    updateVisibility();
}

function createStatusBadge(status) {
    const normalized = STATUS_META[status] ? status : "unknown";
    const meta = STATUS_META[normalized];

    return `<span class="inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-semibold uppercase tracking-wide ${meta.classes}">${meta.label}</span>`;
}

function createVersionLink(version, status) {
    if (status === "unsupported") {
        return `<a class="font-medium text-rose-700 underline decoration-2 underline-offset-4 hover:text-rose-900 dark:text-rose-300 dark:hover:text-rose-200" href="${URLS.issues}" target="_blank" rel="noopener noreferrer">Issues</a>`;
    }

    const readmeUrl = URLS.readme.replace("{version}", encodeURIComponent(version));
    return `<a class="font-medium text-sky-700 underline decoration-2 underline-offset-4 hover:text-sky-900 dark:text-sky-300 dark:hover:text-sky-200" href="${readmeUrl}" target="_blank" rel="noopener noreferrer">README</a>`;
}

function setCounts(entries) {
    const counts = {
        supported: 0,
        disabled: 0,
        unsupported: 0
    };

    for (const [, status] of entries) {
        if (Object.prototype.hasOwnProperty.call(counts, status)) {
            counts[status] += 1;
        }
    }

    document.getElementById("count-supported").textContent = String(counts.supported);
    document.getElementById("count-disabled").textContent = String(counts.disabled);
    document.getElementById("count-unsupported").textContent = String(counts.unsupported);
}

function setCountsFromPayload(entries, payloadCounts) {
    if (
        payloadCounts
        && typeof payloadCounts === "object"
        && Number.isInteger(payloadCounts.supported)
        && Number.isInteger(payloadCounts.disabled)
        && Number.isInteger(payloadCounts.unsupported)
    ) {
        document.getElementById("count-supported").textContent = String(payloadCounts.supported);
        document.getElementById("count-disabled").textContent = String(payloadCounts.disabled);
        document.getElementById("count-unsupported").textContent = String(payloadCounts.unsupported);
        return;
    }

    setCounts(entries);
}

function parsePayload(payload) {
    if (payload && typeof payload === "object" && payload.versions && typeof payload.versions === "object") {
        return {
            entries: Object.entries(payload.versions),
            counts: payload.counts,
            generatedAt: typeof payload.generated_at === "string" ? payload.generated_at : null
        };
    }

    return {
        entries: Object.entries(payload || {}),
        counts: null,
        generatedAt: null
    };
}

function formatLastCheck(generatedAt) {
    if (!generatedAt) {
        return "Last check: unknown";
    }

    const date = new Date(generatedAt);
    if (Number.isNaN(date.getTime())) {
        return `Last check: ${generatedAt}`;
    }

    const now = new Date();
    const diffSeconds = Math.max(0, Math.floor((now.getTime() - date.getTime()) / 1000));

    let relative = "just now";
    if (diffSeconds >= 31536000) {
        const years = Math.floor(diffSeconds / 31536000);
        relative = `${years} year${years === 1 ? "" : "s"} ago`;
    } else if (diffSeconds >= 2592000) {
        const months = Math.floor(diffSeconds / 2592000);
        relative = `${months} month${months === 1 ? "" : "s"} ago`;
    } else if (diffSeconds >= 604800) {
        const weeks = Math.floor(diffSeconds / 604800);
        relative = `${weeks} week${weeks === 1 ? "" : "s"} ago`;
    } else if (diffSeconds >= 86400) {
        const days = Math.floor(diffSeconds / 86400);
        relative = `${days} day${days === 1 ? "" : "s"} ago`;
    } else if (diffSeconds >= 3600) {
        const hours = Math.floor(diffSeconds / 3600);
        relative = `${hours} hour${hours === 1 ? "" : "s"} ago`;
    } else if (diffSeconds >= 60) {
        const minutes = Math.floor(diffSeconds / 60);
        relative = `${minutes} minute${minutes === 1 ? "" : "s"} ago`;
    }

    const absolute = date.toLocaleString("en-US", {
        dateStyle: "medium",
        timeStyle: "medium"
    });

    return `Last check: ${relative} (${absolute})`;
}

function renderRows(entries) {
    tableBody.textContent = "";

    const fragment = document.createDocumentFragment();

    entries.forEach(([version, status]) => {
        const row = document.createElement("tr");
        row.className = "transition hover:bg-slate-50/80 dark:hover:bg-slate-800/60";

        const versionCell = document.createElement("td");
        versionCell.className = "px-4 py-3 font-mono text-sm text-slate-900 dark:text-slate-100";
        versionCell.textContent = version;

        const statusCell = document.createElement("td");
        statusCell.className = "px-4 py-3";
        statusCell.innerHTML = createStatusBadge(status);

        const linkCell = document.createElement("td");
        linkCell.className = "px-4 py-3 text-slate-700 dark:text-slate-200";
        linkCell.innerHTML = createVersionLink(version, status);

        row.appendChild(versionCell);
        row.appendChild(statusCell);
        row.appendChild(linkCell);
        fragment.appendChild(row);
    });

    tableBody.appendChild(fragment);
}

function setupDataTable() {
    if (!versionsTable || !window.simpleDatatables || !window.simpleDatatables.DataTable) {
        return;
    }

    if (versionsDataTable) {
        versionsDataTable.destroy();
        versionsDataTable = null;
    }

    versionsDataTable = new window.simpleDatatables.DataTable(versionsTable, {
        searchable: true,
        sortable: true,
        perPage: 15,
        perPageSelect: [10, 15, 25, 50, 100],
        labels: {
            placeholder: "Search versions...",
            perPage: "per page",
            noRows: "No versions found",
            info: "Showing {start} to {end} of {rows} versions"
        }
    });
}

async function loadData() {
    try {
        const response = await fetch("./version_support_status.json", { cache: "no-store" });
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const payload = await response.json();
        const { entries, counts, generatedAt } = parsePayload(payload);

        renderRows(entries);
        setupDataTable();
        setCountsFromPayload(entries, counts);
        loadState.textContent = formatLastCheck(generatedAt);
    } catch (error) {
        if (versionsDataTable) {
            versionsDataTable.destroy();
            versionsDataTable = null;
        }

        tableBody.innerHTML = `
        <tr>
            <td colspan="3" class="px-4 py-5 text-sm text-rose-700">Failed to load version_support_status.json. Please reload the page.</td>
        </tr>
        `;
        loadState.textContent = "Loading failed.";
        console.error(error);
    }
}

setupTheme();
setupScrollTopButton();
loadData();
