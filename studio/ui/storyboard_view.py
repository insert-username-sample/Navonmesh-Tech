import flet as ft
import json
import os
import asyncio

class StoryboardView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.state_file = "studio/assets/storyboard_state.json"
        self.segments = self._load_segments()
        self.controls = self._build_controls()

    def _load_segments(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    blocks = data.get("blocks", [])
                    for b in blocks:
                        if "duration" not in b:
                            b["duration"] = "0:30"
                        if "script_en" not in b:
                            b["script_en"] = ""
                        if "script_hi" not in b:
                            b["script_hi"] = ""
                    return blocks
            except Exception:
                pass
        return []

    async def _save_segments(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump({"blocks": self.segments, "last_updated": "Live Sync"}, f, indent=4)
        except Exception as e:
            print(f"[STORYBOARD] Save Error: {e}")

    def _build_controls(self):
        return [
            ft.Row(
                [
                    ft.Column([
                        ft.Text("PROJECT STORM-AI", size=14, color="#00F5FF", weight=ft.FontWeight.W_900),
                        ft.Text("Autonomous Script: Tech Signal V24", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ]),
                    ft.ElevatedButton(
                        "LAUNCH PRODUCTION", 
                        icon=ft.Icons.ROCKET,
                        bgcolor="#00F5FF",
                        color="#000000",
                        on_click=self._on_launch_production,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.padding.symmetric(20, 15)
                        )
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(height=40, color="#1F1F23"),
            ft.ListView(
                expand=True,
                spacing=15,
                padding=10,
                controls=[self._create_premium_segment_card(s) for s in self.segments],
            ),
        ]

    def _create_premium_segment_card(self, segment):
        return ft.Container(
            padding=15,
            border_radius=12,
            border=ft.border.all(1, "#1F1F23"),
            bgcolor="#111113",
            on_hover=self._on_card_hover,
            content=ft.Row(
                [
                    ft.Container(
                        width=140,
                        height=80,
                        bgcolor="#070708",
                        border_radius=8,
                        border=ft.border.all(1, "#1F1F23"),
                        content=ft.Stack([
                            ft.Container(
                                content=ft.Icon(ft.Icons.IMAGE_ROUNDED, size=24, color="#1F1F23"),
                                alignment="center",
                                expand=True
                            ),
                            ft.Container(
                                content=ft.Text(segment.get("duration", "0:30"), size=10, color=ft.Colors.WHITE70),
                                alignment="bottom_right",
                                padding=5,
                                bgcolor="black38",
                            )
                        ]),
                    ),
                    ft.VerticalDivider(width=20, color="#1F1F23"),
                    ft.Column(
                        [
                            ft.Text(segment["title"], size=17, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(segment["type"], size=9, weight=ft.FontWeight.BOLD, color="#00F5FF"),
                                        padding=ft.padding.symmetric(2, 6),
                                        border=ft.border.all(1, "#00F5FF"),
                                        border_radius=4,
                                    ),
                                    ft.Text(f"STATION: {segment['status']}", size=11, color=ft.Colors.GREY_500),
                                ],
                                spacing=10,
                            ),
                        ],
                        expand=True,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT_DOCUMENT, 
                                icon_color="#00F5FF", 
                                tooltip="Edit Visual Script",
                                data=segment,
                                on_click=self._on_edit_click
                            ),
                            ft.IconButton(
                                icon=ft.Icons.AUDIO_FILE, 
                                icon_color=ft.Colors.GREY_600, 
                                tooltip="Generate Audio Preview",
                                data="Audio Preview",
                                on_click=self._on_placeholder_click
                            ),
                            ft.IconButton(
                                icon=ft.Icons.MOVIE_FILTER, 
                                icon_color=ft.Colors.GREY_600, 
                                tooltip="Pre-render Segment",
                                data="Render Segment",
                                on_click=self._on_placeholder_click
                            ),
                            ft.VerticalDivider(width=10, color="#1F1F23"),
                            ft.IconButton(
                                icon=ft.Icons.PLAY_CIRCLE_FILL, 
                                icon_color=ft.Colors.GREY_400, 
                                icon_size=32,
                                tooltip="Final Preview",
                                data="Final Preview",
                                on_click=self._on_placeholder_click
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    async def _open_script_editor(self, segment):
        # Async Dialog State
        en_input = ft.TextField(label="English Script", value=segment.get("script_en", ""), multiline=True, min_lines=3, bgcolor="#0A0A0B", border_color="#1F1F23")
        hi_input = ft.TextField(label="Hindi Script", value=segment.get("script_hi", ""), multiline=True, min_lines=3, bgcolor="#0A0A0B", border_color="#1F1F23")

        async def save_close(e):
            segment["script_en"] = en_input.value
            segment["script_hi"] = hi_input.value
            segment["status"] = "User Refined"
            await self._save_segments()
            self.page.dialog.open = False
            asyncio.create_task(self.refresh_ui())
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Script Editor: {segment['title']}"),
            content=ft.Column([
                ft.Text("Fine-tune the agentic output below.", size=12, color=ft.Colors.GREY_500),
                en_input,
                hi_input
            ], spacing=15, height=400, width=600),
            actions=[
                ft.TextButton("CANCEL", on_click=self._close_dialog),
                ft.ElevatedButton("SAVE CHANGES", bgcolor="#00F5FF", color="#000000", on_click=save_close),
            ],
            bgcolor="#111113",
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    async def _close_dialog(self, e=None):
        self.page.dialog.open = False
        self.page.update()

    async def _on_launch_production(self, e):
        from studio.core.auto_pipeline import AutoPipeline
        pipeline = AutoPipeline()

        self.page.snack_bar = ft.SnackBar(ft.Text("SYSTEM: Launching VRAM-Locked Production Pipeline..."), bgcolor="#111113")
        self.page.snack_bar.open = True
        self.page.update()

        async def run_task():
            try:
                await pipeline.run_full_production(page=self.page)
                self.page.snack_bar = ft.SnackBar(ft.Text("SYSTEM: Production Complete. Check daily_shorts/"), bgcolor="#00F5FF")
                self.page.snack_bar.open = True
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"ERROR: Production Failed! {ex}"), bgcolor=ft.Colors.RED_700)
                self.page.snack_bar.open = True
            self.page.update()

        # Reliable background task execution
        self.page.run_task(run_task)

    async def _on_edit_click(self, e):
        segment = e.control.data
        print(f"[STORYBOARD] Triggering Script Editor for: {segment['title']}")
        await self._open_script_editor(segment)

    async def _on_placeholder_click(self, e):
        label = e.control.data
        self.page.snack_bar = ft.SnackBar(ft.Text(f"ACTION: {label} (Feature in Roadmap Phase 2)"), bgcolor="#111113")
        self.page.snack_bar.open = True
        self.page.update()

    def _on_card_hover(self, e):
        e.control.border = ft.border.all(1, "#00F5FF" if e.data == "true" else "#1F1F23")
        e.control.update()

    async def refresh_ui(self):
        print("[STORYBOARD] Refreshing UI...")
        self.segments = self._load_segments()
        self.controls = self._build_controls()
        if self.page:
            self.update()
