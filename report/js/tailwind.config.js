tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                support: {
                    bg: "#e6f7ec",
                    fg: "#0f5f3a",
                    border: "#8ad3a8"
                },
                disabled: {
                    bg: "#fff7e8",
                    fg: "#8a4d00",
                    border: "#f0c27d"
                },
                unsupported: {
                    bg: "#ffecec",
                    fg: "#8a1f1f",
                    border: "#f0a3a3"
                },
                unknown: {
                    bg: "#eef0f4",
                    fg: "#4b5563",
                    border: "#cbd5e1"
                }
            },
            boxShadow: {
                pane: "0 12px 30px rgba(18, 28, 45, 0.08)"
            }
        }
    }
};
