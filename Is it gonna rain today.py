import requests
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

console = Console()

def get_dhaka_hourly_rain():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 23.7104,
        "longitude": 90.4074,
        "hourly": ["precipitation_probability", "precipitation"],
        "timezone": "auto",
        "forecast_days": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "hourly" not in data:
            return Panel("[bold red]API Error:[/bold red] Data unavailable.", border_style="red")

        hourly_data = data['hourly']
        current_dt = datetime.now()
        # API uses 2026-03-16T14:00 format
        current_hour_tag = current_dt.strftime("%Y-%m-%dT%H:00")
        
        title_text = f"Dhaka Rain Forecast — {current_dt.strftime('%a, %b %d, %Y')}"
        
        table = Table(title=title_text, title_style="bold cyan", header_style="bold magenta")
        table.add_column("Time", justify="center")
        table.add_column("Chance (%)", justify="center")
        table.add_column("Amount (mm)", justify="center")

        for i in range(len(hourly_data['time'])):
            raw_time = hourly_data['time'][i]
            prob = hourly_data['precipitation_probability'][i]
            amount = hourly_data['precipitation'][i]
            
            dt_obj = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M")
            clean_time = dt_obj.strftime("%I:%M %p")
            
            # Use Text objects to avoid the [ / ] tag crashing the script
            time_text = Text(clean_time)
            prob_text = Text(f"{prob}%")
            amount_text = Text(f"{amount}mm")

            # Apply colors
            if prob > 50:
                prob_text.stylize("bold red")
            
            if amount > 2.0:
                amount_text.stylize("bold red")
            elif amount > 0:
                amount_text.stylize("bold yellow")
            else:
                amount_text.stylize("green")

            # Highlight the current hour row
            row_style = "bold reverse underline" if raw_time == current_hour_tag else ""
            
            table.add_row(time_text, prob_text, amount_text, style=row_style)
        
        return table

    except Exception as e:
        return Panel(f"[bold red]Error:[/bold red] {str(e)}", border_style="red")

if __name__ == "__main__":
    try:
        # screen=True works now because we are using proper style application
        with Live(get_dhaka_hourly_rain(), refresh_per_second=1, screen=True) as live:
            while True:
                live.update(get_dhaka_hourly_rain())
                time.sleep(300)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        console.print(f"\n[bold red]CRITICAL ERROR:[/bold red] {e}")
        input("Press Enter to exit...")
