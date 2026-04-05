import flet as ft
import asyncio
import json
import os
from studio.ui.storyboard_view import StoryboardView

def main(page: ft.Page):
    page.title = "NAVONMESH | Agentic Newsroom Studio"
    page.bgcolor = "#0A0A0B"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    # Window dimensions for better testing layout
    page.window.width = 1440
    page.window.height = 900

    # --- AUTONOMOUS STARTUP ---
    async def initial_scout(e=None):
        from studio.core.news_scout import NewsScout
        from studio.core.brain_adapter import BrainAdapter

        print("[STUDIO] Triggering Autonomous Scout...")
        page.snack_bar = ft.SnackBar(ft.Text("SYSTEM: Scout Agent Scanning Trends..."), bgcolor="#111113")
        page.snack_bar.open = True
        page.update()

        scout = NewsScout()
        brain = BrainAdapter()
        
        # Scout & Draft (Keep in background)
        signals = await scout.scout_signals()
        blocks = brain.draft_storyboard(signals)
        
        # Save to state
        os.makedirs("studio/assets", exist_ok=True)
        with open("studio/assets/storyboard_state.json", "w") as f:
            json.dump({"blocks": blocks, "last_updated": "Live Now"}, f, indent=4)
        
        # Refresh Storyboard (UI update)
        await storyboard.refresh_ui()
        
        page.snack_bar = ft.SnackBar(ft.Text("SYSTEM: Intelligence Feed Refreshed with 3 News Signals."), bgcolor="#00F5FF")
        page.snack_bar.open = True
        page.update()
        print("[STUDIO] Intelligence Feed Refreshed.")

    # --- UI COMPONENTS ---
    storyboard = StoryboardView()
    content_area = ft.Container(expand=True)
    content_area.content = storyboard

    # --- NAVIGATION LOGIC ---
    def switch_view(idx):
        print(f"[NAV] Switching to View ID: {idx}")
        # Always clear dialogs on major view switch
        page.dialog = None
        
        # Switch content
        if idx == 0 or idx == 1:
            content_area.content = storyboard
        elif idx == 2:
            content_area.content = ft.Container(
                content=ft.Column([
                    ft.Text("PRODUCTION QUEUE", size=24, weight="bold", color="#00F5FF"),
                    ft.Text("Monitoring RTX 3060 Ti | Local Rendering Factory", color="grey", size=12),
                    ft.Divider(height=20, color="#1F1F23"),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Job ID")),
                            ft.DataColumn(ft.Text("Format")),
                            ft.DataColumn(ft.Text("Status")),
                            ft.DataColumn(ft.Text("Progress")),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("STORM-V24-001")),
                                ft.DataCell(ft.Text("Short (9:16)")),
                                ft.DataCell(ft.Text("PENDING", color=ft.Colors.AMBER_400)),
                                ft.DataCell(ft.ProgressBar(value=0, width=100, color="#00F5FF")),
                            ]),
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text("STORM-V24-002")),
                                ft.DataCell(ft.Text("Master (4K)")),
                                ft.DataCell(ft.Text("IDLE", color=ft.Colors.GREY_600)),
                                ft.DataCell(ft.ProgressBar(value=0, width=100, color="#1F1F23")),
                            ]),
                        ],
                        bgcolor="#111113",
                        border=ft.border.all(1, "#1F1F23"),
                        border_radius=10,
                    )
                ], spacing=10),
                padding=20
            )
        
        page.update()

    def on_nav_change(e):
        switch_view(e.control.selected_index)

    # --- SIDEBAR & HEADER ---
    sidebar = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        bgcolor="#0D0D0E",
        on_change=on_nav_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.LIGHT_MODE_ROUNDED, color=ft.Colors.GREY_600),
                selected_icon=ft.Icon(ft.Icons.LIGHT_MODE_ROUNDED, color="#00F5FF"),
                label="Feed"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.DASHBOARD_ROUNDED, color=ft.Colors.GREY_600),
                selected_icon=ft.Icon(ft.Icons.DASHBOARD_ROUNDED, color="#00F5FF"),
                label="Storyboard"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(ft.Icons.VIDEO_LIBRARY_ROUNDED, color=ft.Colors.GREY_600),
                selected_icon=ft.Icon(ft.Icons.VIDEO_LIBRARY_ROUNDED, color="#00F5FF"),
                label="Queue"
            ),
        ],
    )

    # System Status Header
    header = ft.Container(
        content=ft.Row([
            ft.Text("NAVONMESH", size=22, weight="bold", color="#00F5FF"),
            ft.Text("STUDIO Alpha", size=12, color="grey"),
            ft.VerticalDivider(width=20),
            ft.Text("RTX 3060 Ti | 8GB VRAM", size=10, color="grey"),
            ft.Row(expand=True),
            # Pulse Indicator to prove Backend-to-Frontend communication
            ft.Container(bgcolor="#00F5FF", border_radius=10, width=8, height=8),
            ft.Text("CORE-01 ALIVE", size=10, color="grey"),
            ft.IconButton(ft.Icons.REFRESH, icon_color="grey", on_click=lambda _: page.run_task(initial_scout)),
        ]),
        padding=15,
        bgcolor="#111113",
        border=ft.border.only(bottom=ft.border.BorderSide(1, "#1F1F23"))
    )

    page.add(
        ft.Column([
            header,
            ft.Row([
                sidebar,
                content_area
            ], expand=True)
        ], expand=True)
    )

    # Initial scout in background
    page.run_task(initial_scout)

if __name__ == "__main__":
    # Explicit loop management for Flet on Windows
    try:
        # Standard launch with web browser view
        # We explicitly bind to 127.0.0.1 to avoid WebSocket resolution issues in some local environments
        ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8550, host="127.0.0.1")
    except Exception as e:
        print(f"[FATAL] Studio failed to launch: {e}")
