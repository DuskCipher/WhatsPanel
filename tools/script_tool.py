# tools/script_tool.py

import streamlit as st
from streamlit_option_menu import option_menu
from tools.generate_script import show_generate_script
from tools.edit_script import show_edit_script
from tools.test_script import show_test_script
from tools.encryption_tool import show_encryption_tool
from tools.library_tools import show_library_tools
from tools.script_analyzer import show_script_analyzer
from tools.script_utilities import show_script_utilities
from tools.export_import_script import show_export_import_script

def show_script_tool():
    st.markdown("""
        <style>
        .script-title {
            text-align: center;
            font-size: 38px;
            font-weight: 800;
            letter-spacing: 1px;
            color: #ffffff;
            text-transform: uppercase;
            margin-bottom: 20px;
        }
        .menu-scroll {
            overflow-x: auto;
            white-space: nowrap;
            padding-bottom: 5px;
            display: flex;
            justify-content: center;
        }
        .option-menu .nav-link-active i {
            display: none !important;
        }
        .option-menu .nav-link span {
            width: 100%;
            display: inline-block;
            text-align: center;
        }
        </style>
        <div class='script-title'>🛠️ Script Tool Duskcipher 0.1</div>
        <div class="menu-scroll">
    """, unsafe_allow_html=True)

    submenu = option_menu(
        menu_title=None,
        options=[
            "Generate Script Otomatis",
            "Edit Script",
            "Test Script",
            "Library Tools",
            "Script Analyzer",
            "Script Utilities",
            "Encrypt / Decrypt Script",
            "Export / Import Script"
        ],
        icons=[
            "lightning", "pencil", "bug", "briefcase", "search", "tools", "shield-lock", "arrow-down-up"
        ],
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#111111",
                "display": "inline-block",
                "white-space": "nowrap"
            },
            "icon": {
                "color": "#FFA500",
                "font-size": "18px",
                "text-align": "center"
            },
            "nav-link": {
                "font-size": "13.5px",
                "text-align": "center",
                "margin": "5px",
                "padding": "10px 20px",
                "color": "#CCCCCC",
                "--hover-color": "#2a2a2a",
                "border-radius": "8px",
                "white-space": "nowrap"
            },
            "nav-link-selected": {
                "background-color": "#FFA500",
                "color": "black",
                "font-weight": "bold",
                "text-align": "center",
                "white-space": "nowrap"
            }
        }
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if submenu == "Generate Script Otomatis":
        show_generate_script()
    elif submenu == "Edit Script":
        show_edit_script()
    elif submenu == "Test Script":
        show_test_script()
    elif submenu == "Encrypt / Decrypt Script":
        show_encryption_tool()
    elif submenu == "Library Tools":
        show_library_tools()
    elif submenu == "Script Analyzer":
        show_script_analyzer()
    elif submenu == "Script Utilities":
        show_script_utilities()
    elif submenu == "Export / Import Script":
        show_export_import_script()
    else:
        st.warning("❗ Submenu tidak dikenal.")
