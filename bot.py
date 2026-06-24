import logging
import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuration and basic logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

DATA_FILE = "fares.json"

def load_data():
    """Load stored fare data from a local JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "CBD-Rongai": [100, 120, 150],
        "CBD-Thika": [80, 100, 120],
        "CBD-Kikuyu": [70, 80, 100]
    }

def save_data(data):
    """Save updated fare data to a local JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# Initialize state
fare_data = load_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message and command listing."""
    welcome_text = (
        "🚌 Welcome to Matatu Fare Bot 2026!\n"
        "Real-time crowdsourced peak hour fares for Nairobi commuters.\n\n"
        "Available Commands:\n"
        "/fare <route> - Get current average fare\n"
        "/report <route> <amount> - Submit a fare update\n"
        "/routes - List all active routes\n"
        "/help - Show usage guidelines"
    )
    await update.message.reply_text(welcome_text)

async def get_fare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Calculate and return the average fare for a specific route."""
    if not context.args:
        await update.message.reply_text("❌ Please specify a route. Example: /fare CBD-Rongai")
        return
    
    route = " ".join(context.args).strip()
    if route in fare_data:
        fares = fare_data[route]
        avg = sum(fares) / len(fares)
        peak_max = max(fares)
        await update.message.reply_text(
            f"📍 Route: {route}\n"
            f"💰 Average Fare: KES {avg:.2f}\n"
            f"🔥 Peak Max: KES {peak_max:.2f}\n"
            f"📊 Based on {len(fares)} reports."
        )
    else:
        await update.message.reply_text(f"❓ Route '{route}' not found. Be the first to /report it!")

async def report_fare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Allow users to contribute fare data to the crowdsourced database."""
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /report <route-name> <amount>")
        return
    
    try:
        amount = float(context.args[-1])
        route = " ".join(context.args[:-1]).strip()
        
        if route not in fare_data:
            fare_data[route] = []
            
        fare_data[route].append(amount)
        save_data(fare_data)
        
        await update.message.reply_text(f"✅ Recorded KES {amount} for {route}. Asante for reporting!")
    except ValueError:
        await update.message.reply_text("❌ Invalid amount. Please enter a numeric value.")

async def list_routes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display all routes currently stored in the system."""
    if not fare_data:
        await update.message.reply_text("No routes tracked yet.")
        return
    
    routes_str = "\n".join([f"• {r} ({len(v)} reports)" for r, v in fare_data.items()])
    await update.message.reply_text(f"🌍 Currently Tracked Routes:\n{routes_str}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Detailed documentation for the user."""
    help_text = (
        "How to use Matatu Fare Bot:\n\n"
        "1. Always use route names consistently (e.g., 'CBD-Kitengela').\n"
        "2. Report the fare you just paid to keep data fresh.\n"
        "3. Average fares help you negotiate or plan your commute during peak hours."
    )
    await update.message.reply_text(help_text)

if __name__ == '__main__':
    # Retrieve token from environment variable
    TOKEN = os.getenv("TELEGRAM_TOKEN", "REPLACE_WITH_YOUR_BOT_TOKEN")
    
    if TOKEN == "REPLACE_WITH_YOUR_BOT_TOKEN":
        print("Error: Please set the TELEGRAM_TOKEN environment variable.")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Add command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("fare", get_fare))
        app.add_handler(CommandHandler("report", report_fare))
        app.add_handler(CommandHandler("routes", list_routes))
        app.add_handler(CommandHandler("help", help_command))
        
        print("Matatu Fare Bot is online...")
        app.run_polling()