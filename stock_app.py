"""
Main GUI application for Stock Record Keeping.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import os
import shutil
from PIL import Image, ImageTk
from database import StockDatabase
from stock_data import StockDataFetcher

# Constants
REVIEW_ALERT_DAYS = 30  # Days before review alert
EARNINGS_ALERT_DAYS = 7  # Days before earnings alert

# Position status options
POSITION_STATUSES = [
    "INCREASE",
    "HOLD (Green)",
    "HOLD (Red)",
    "INVESTIGATION REQUIRED",
    "DECREASE",
    "SOLD"
]

# Status colors
STATUS_COLORS = {
    "INCREASE": "#00C853",  # Green
    "HOLD (Green)": "#4CAF50",  # Light Green
    "HOLD (Red)": "#FF5252",  # Red
    "INVESTIGATION REQUIRED": "#FFC107",  # Amber
    "DECREASE": "#FF6D00",  # Orange
    "SOLD": "#9E9E9E"  # Gray
}


class StockApp:
    """Main Stock Record Keeping Application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Record Keeping")
        self.root.geometry("1200x700")
        
        self.db = StockDatabase()
        self.fetcher = StockDataFetcher()
        self.current_sort = "id"
        self.selected_image_path = None
        
        # Create images directory
        self.images_dir = "stocks_images"
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
        
        self.setup_ui()
        self.refresh_stock_list()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title and controls
        self.setup_header(main_frame)
        
        # Stock list
        self.setup_stock_list(main_frame)
        
        # Buttons
        self.setup_buttons(main_frame)
    
    def setup_header(self, parent):
        """Set up header with title and sorting options."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        title = ttk.Label(header_frame, text="Stock Portfolio", font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, sticky=tk.W)
        
        # Sort controls
        sort_frame = ttk.Frame(header_frame)
        sort_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Label(sort_frame, text="Sort by:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.sort_var = tk.StringVar(value="Recent")
        sort_options = [
            ("Recent", "id"),
            ("Name", "name"),
            ("Ticker", "ticker"),
            ("Total Value", "value"),
            ("% Change", "percent"),
            ("Status", "status"),
            ("Last Reviewed", "reviewed")
        ]
        
        sort_menu = ttk.Combobox(sort_frame, textvariable=self.sort_var, 
                                 values=[opt[0] for opt in sort_options],
                                 state="readonly", width=15)
        sort_menu.pack(side=tk.LEFT, padx=(0, 5))
        sort_menu.bind("<<ComboboxSelected>>", self.on_sort_change)
        
        ttk.Button(sort_frame, text="Refresh Prices", 
                  command=self.refresh_all_prices).pack(side=tk.LEFT)
    
    def setup_stock_list(self, parent):
        """Set up the stock list treeview."""
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical")
        hsb = ttk.Scrollbar(list_frame, orient="horizontal")
        
        # Treeview
        columns = ("ticker", "name", "amount", "price_paid", "current_value", 
                  "total_value", "change", "status", "last_reviewed")
        
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings",
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Column headings
        self.tree.heading("ticker", text="Ticker")
        self.tree.heading("name", text="Stock Name")
        self.tree.heading("amount", text="Shares")
        self.tree.heading("price_paid", text="Price Paid")
        self.tree.heading("current_value", text="Current Price")
        self.tree.heading("total_value", text="Total Value")
        self.tree.heading("change", text="% Change")
        self.tree.heading("status", text="Status")
        self.tree.heading("last_reviewed", text="Last Reviewed")
        
        # Column widths
        self.tree.column("ticker", width=80)
        self.tree.column("name", width=200)
        self.tree.column("amount", width=80)
        self.tree.column("price_paid", width=100)
        self.tree.column("current_value", width=100)
        self.tree.column("total_value", width=120)
        self.tree.column("change", width=100)
        self.tree.column("status", width=150)
        self.tree.column("last_reviewed", width=150)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Bind double-click
        self.tree.bind("<Double-1>", self.on_stock_double_click)
        
        # Configure tags for row colors
        for status, color in STATUS_COLORS.items():
            self.tree.tag_configure(status, background=color, foreground="white")
    
    def setup_buttons(self, parent):
        """Set up action buttons."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Stock", 
                  command=self.add_stock_dialog).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Edit Stock", 
                  command=self.edit_stock_dialog).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Delete Stock", 
                  command=self.delete_stock).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Mark Reviewed", 
                  command=self.mark_reviewed).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="View Details", 
                  command=self.view_details).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(button_frame, text="Check Alerts", 
                  command=self.check_alerts).pack(side=tk.LEFT, padx=(0, 5))
    
    def refresh_stock_list(self):
        """Refresh the stock list from database."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get stocks from database
        stocks = self.db.get_all_stocks(sort_by=self.current_sort)
        
        for stock in stocks:
            # Calculate values
            current_price = stock['current_value'] or stock['price_paid']
            total_value = stock['amount'] * current_price
            
            if stock['price_change_percent'] is not None:
                change_str = f"{stock['price_change_percent']:+.2f}%"
            else:
                change_percent = ((current_price - stock['price_paid']) / stock['price_paid'] * 100) if stock['price_paid'] != 0 else 0
                change_str = f"{change_percent:+.2f}%"
            
            # Format last reviewed date
            try:
                reviewed_dt = datetime.fromisoformat(stock['last_reviewed_date'])
                days_ago = (datetime.now() - reviewed_dt).days
                if days_ago == 0:
                    reviewed_str = "Today"
                elif days_ago == 1:
                    reviewed_str = "Yesterday"
                else:
                    reviewed_str = f"{days_ago} days ago"
            except (ValueError, TypeError):
                reviewed_str = "Unknown"
            
            values = (
                stock['ticker'],
                stock['stock_name'],
                stock['amount'],
                f"${stock['price_paid']:.2f}",
                f"${current_price:.2f}",
                f"${total_value:.2f}",
                change_str,
                stock['position_status'],
                reviewed_str
            )
            
            # Insert with status color tag
            self.tree.insert("", "end", iid=stock['id'], values=values, 
                           tags=(stock['position_status'],))
    
    def on_sort_change(self, event=None):
        """Handle sort option change."""
        sort_label = self.sort_var.get()
        sort_map = {
            "Recent": "id",
            "Name": "name",
            "Ticker": "ticker",
            "Total Value": "value",
            "% Change": "percent",
            "Status": "status",
            "Last Reviewed": "reviewed"
        }
        self.current_sort = sort_map.get(sort_label, "id")
        self.refresh_stock_list()
    
    def add_stock_dialog(self):
        """Open dialog to add a new stock."""
        self.stock_dialog(mode="add")
    
    def edit_stock_dialog(self):
        """Open dialog to edit selected stock."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a stock to edit.")
            return
        
        stock_id = int(selection[0])
        stock = self.db.get_stock(stock_id)
        self.stock_dialog(mode="edit", stock=stock)
    
    def stock_dialog(self, mode="add", stock=None):
        """Open stock entry/edit dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Stock" if mode == "add" else "Edit Stock")
        dialog.geometry("600x750")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Create form
        form_frame = ttk.Frame(dialog, padding="10")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        row = 0
        
        # Stock name
        ttk.Label(form_frame, text="Stock Name:").grid(row=row, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=stock['stock_name'] if stock else "")
        name_entry = ttk.Entry(form_frame, textvariable=name_var, width=40)
        name_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Ticker
        ttk.Label(form_frame, text="Ticker:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ticker_var = tk.StringVar(value=stock['ticker'] if stock else "")
        ticker_entry = ttk.Entry(form_frame, textvariable=ticker_var, width=40)
        ticker_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Fetch info button
        def fetch_stock_info():
            ticker = ticker_var.get().strip().upper()
            if ticker:
                info = self.fetcher.get_stock_info(ticker)
                data_fetched = False
                if info.get('name') and info['name'] != ticker:
                    name_var.set(info['name'])
                    data_fetched = True
                if info.get('current_price'):
                    current_value_var.set(f"{info['current_price']:.2f}")
                    data_fetched = True
                
                if data_fetched:
                    messagebox.showinfo("Success", f"Fetched data for {ticker}")
                else:
                    messagebox.showwarning("No Data", f"Could not fetch data for {ticker}. Check ticker or network connection.")
        
        ttk.Button(form_frame, text="Fetch Info", command=fetch_stock_info).grid(row=row, column=2, padx=5)
        row += 1
        
        # Price paid
        ttk.Label(form_frame, text="Price Paid ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        price_var = tk.StringVar(value=str(stock['price_paid']) if stock else "0.00")
        price_entry = ttk.Entry(form_frame, textvariable=price_var, width=40)
        price_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Amount (shares)
        ttk.Label(form_frame, text="Shares:").grid(row=row, column=0, sticky=tk.W, pady=5)
        amount_var = tk.StringVar(value=str(stock['amount']) if stock else "0")
        amount_entry = ttk.Entry(form_frame, textvariable=amount_var, width=40)
        amount_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Current value
        ttk.Label(form_frame, text="Current Price ($):").grid(row=row, column=0, sticky=tk.W, pady=5)
        current_value_var = tk.StringVar(value=str(stock['current_value']) if stock and stock['current_value'] else "")
        current_value_entry = ttk.Entry(form_frame, textvariable=current_value_var, width=40)
        current_value_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Position status
        ttk.Label(form_frame, text="Position Status:").grid(row=row, column=0, sticky=tk.W, pady=5)
        status_var = tk.StringVar(value=stock['position_status'] if stock else POSITION_STATUSES[0])
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=POSITION_STATUSES, state="readonly", width=37)
        status_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Earnings date
        ttk.Label(form_frame, text="Earnings Date:").grid(row=row, column=0, sticky=tk.W, pady=5)
        earnings_var = tk.StringVar(value=stock['earnings_date'] if stock and stock['earnings_date'] else "")
        earnings_entry = ttk.Entry(form_frame, textvariable=earnings_var, width=40)
        earnings_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(form_frame, text="(YYYY-MM-DD or blank)", font=('Arial', 8)).grid(row=row, column=2, sticky=tk.W)
        row += 1
        
        # Notes
        ttk.Label(form_frame, text="Notes:").grid(row=row, column=0, sticky=(tk.W, tk.N), pady=5)
        notes_text = tk.Text(form_frame, width=40, height=5)
        notes_text.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5)
        if stock and stock['notes']:
            notes_text.insert("1.0", stock['notes'])
        row += 1
        
        # Image
        self.selected_image_path = stock['image_path'] if stock else None
        image_label_var = tk.StringVar(value="No image" if not self.selected_image_path else os.path.basename(self.selected_image_path))
        
        ttk.Label(form_frame, text="Image:").grid(row=row, column=0, sticky=tk.W, pady=5)
        image_label = ttk.Label(form_frame, textvariable=image_label_var)
        image_label.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        def select_image():
            filepath = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
            )
            if filepath:
                # Validate that file exists and is readable
                if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
                    self.selected_image_path = filepath
                    image_label_var.set(os.path.basename(filepath))
                else:
                    messagebox.showerror("Error", "Cannot read selected file.")
        
        ttk.Button(form_frame, text="Select Image", command=select_image).grid(row=row, column=2, padx=5)
        row += 1
        
        form_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        def save_stock():
            try:
                stock_name = name_var.get().strip()
                ticker = ticker_var.get().strip().upper()
                price_paid = float(price_var.get())
                amount = int(amount_var.get())
                position_status = status_var.get()
                notes = notes_text.get("1.0", tk.END).strip()
                earnings_date_str = earnings_var.get().strip() or None
                
                # Validate earnings date format if provided
                if earnings_date_str:
                    try:
                        datetime.strptime(earnings_date_str, '%Y-%m-%d')
                    except ValueError:
                        messagebox.showerror("Error", "Earnings date must be in YYYY-MM-DD format.")
                        return
                
                current_value = None
                if current_value_var.get().strip():
                    current_value = float(current_value_var.get())
                
                if not stock_name or not ticker:
                    messagebox.showerror("Error", "Stock name and ticker are required.")
                    return
                
                # Handle image - validate and copy safely
                image_path = ""
                if self.selected_image_path:
                    # Validate image path
                    if not os.path.isfile(self.selected_image_path):
                        messagebox.showerror("Error", "Selected image file not found.")
                        return
                    
                    # Copy image to images directory with safe filename
                    filename = f"{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{os.path.splitext(self.selected_image_path)[1]}"
                    dest_path = os.path.join(self.images_dir, filename)
                    shutil.copy2(self.selected_image_path, dest_path)
                    image_path = dest_path
                
                if mode == "add":
                    self.db.add_stock(stock_name, ticker, price_paid, amount, 
                                     position_status, notes, image_path, current_value, earnings_date_str)
                    messagebox.showinfo("Success", "Stock added successfully!")
                else:
                    stock_id = stock['id']
                    # Keep old image if no new one selected
                    if not self.selected_image_path:
                        image_path = stock['image_path']
                    self.db.update_stock(stock_id, stock_name, ticker, price_paid, 
                                        amount, position_status, notes, image_path, 
                                        current_value, earnings_date_str)
                    messagebox.showinfo("Success", "Stock updated successfully!")
                
                self.refresh_stock_list()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save stock: {e}")
        
        ttk.Button(button_frame, text="Save", command=save_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)
    
    def delete_stock(self):
        """Delete selected stock."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a stock to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this stock?"):
            stock_id = int(selection[0])
            self.db.delete_stock(stock_id)
            self.refresh_stock_list()
            messagebox.showinfo("Success", "Stock deleted successfully!")
    
    def mark_reviewed(self):
        """Mark selected stock as reviewed."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a stock to mark as reviewed.")
            return
        
        stock_id = int(selection[0])
        self.db.update_last_reviewed(stock_id)
        self.refresh_stock_list()
        messagebox.showinfo("Success", "Stock marked as reviewed!")
    
    def view_details(self):
        """View detailed information for selected stock."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a stock to view details.")
            return
        
        stock_id = int(selection[0])
        stock = self.db.get_stock(stock_id)
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Details: {stock['stock_name']}")
        details_window.geometry("600x700")
        
        # Scrollable frame
        canvas = tk.Canvas(details_window)
        scrollbar = ttk.Scrollbar(details_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Details content
        content_frame = ttk.Frame(scrollable_frame, padding="20")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Stock information
        current_price = stock['current_value'] or stock['price_paid']
        total_value = stock['amount'] * current_price
        total_paid = stock['amount'] * stock['price_paid']
        gain_loss = total_value - total_paid
        gain_loss_percent = (gain_loss / total_paid * 100) if total_paid != 0 else 0
        
        details = [
            ("Stock Name", stock['stock_name']),
            ("Ticker", stock['ticker']),
            ("Shares", stock['amount']),
            ("Price Paid", f"${stock['price_paid']:.2f}"),
            ("Current Price", f"${current_price:.2f}"),
            ("Total Paid", f"${total_paid:.2f}"),
            ("Total Value", f"${total_value:.2f}"),
            ("Gain/Loss", f"${gain_loss:+.2f} ({gain_loss_percent:+.2f}%)"),
            ("Position Status", stock['position_status']),
            ("Earnings Date", stock['earnings_date'] or "N/A"),
            ("Last Reviewed", stock['last_reviewed_date']),
            ("Created", stock['created_date']),
            ("Modified", stock['modified_date'])
        ]
        
        for i, (label, value) in enumerate(details):
            ttk.Label(content_frame, text=f"{label}:", font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=(0, 10))
            ttk.Label(content_frame, text=str(value), font=('Arial', 10)).grid(
                row=i, column=1, sticky=tk.W, pady=5)
        
        # Notes
        if stock['notes']:
            row = len(details)
            ttk.Label(content_frame, text="Notes:", font=('Arial', 10, 'bold')).grid(
                row=row, column=0, sticky=(tk.W, tk.N), pady=5, padx=(0, 10))
            notes_label = ttk.Label(content_frame, text=stock['notes'], 
                                   font=('Arial', 10), wraplength=400, justify=tk.LEFT)
            notes_label.grid(row=row, column=1, sticky=tk.W, pady=5)
            row += 1
        
        # Image
        if stock['image_path'] and os.path.exists(stock['image_path']):
            row = len(details) + (1 if stock['notes'] else 0)
            ttk.Label(content_frame, text="Image:", font=('Arial', 10, 'bold')).grid(
                row=row, column=0, sticky=(tk.W, tk.N), pady=5, padx=(0, 10))
            
            try:
                img = Image.open(stock['image_path'])
                img.thumbnail((400, 300))
                photo = ImageTk.PhotoImage(img)
                img_label = ttk.Label(content_frame, image=photo)
                img_label.image = photo  # Keep reference
                img_label.grid(row=row, column=1, sticky=tk.W, pady=5)
            except Exception as e:
                ttk.Label(content_frame, text=f"Error loading image: {e}").grid(
                    row=row, column=1, sticky=tk.W, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Close button
        ttk.Button(details_window, text="Close", 
                  command=details_window.destroy).pack(pady=10)
    
    def refresh_all_prices(self):
        """Refresh current prices for all stocks."""
        stocks = self.db.get_all_stocks()
        
        if not stocks:
            messagebox.showinfo("Info", "No stocks to refresh.")
            return
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Refreshing Prices")
        progress_window.geometry("400x100")
        progress_window.transient(self.root)
        
        ttk.Label(progress_window, text="Fetching current prices...").pack(pady=10)
        progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        
        total = len(stocks)
        updated = 0
        
        for i, stock in enumerate(stocks):
            current_price = self.fetcher.get_current_price(stock['ticker'])
            if current_price:
                change_percent = ((current_price - stock['price_paid']) / stock['price_paid'] * 100) if stock['price_paid'] != 0 else 0
                self.db.update_current_values(stock['id'], current_price, change_percent)
                updated += 1
            
            progress_bar['value'] = ((i + 1) / total) * 100
            progress_window.update()
        
        progress_window.destroy()
        self.refresh_stock_list()
        messagebox.showinfo("Complete", f"Updated {updated} out of {total} stocks.")
    
    def check_alerts(self):
        """Check for stocks that need review."""
        stocks = self.db.get_all_stocks()
        
        alerts = []
        today = datetime.now()
        
        for stock in stocks:
            try:
                last_reviewed = datetime.fromisoformat(stock['last_reviewed_date'])
                days_since_review = (today - last_reviewed).days
                
                # Alert if not reviewed in configured days
                if days_since_review >= REVIEW_ALERT_DAYS:
                    alerts.append(f"• {stock['ticker']} ({stock['stock_name']}) - Not reviewed for {days_since_review} days")
                
                # Check for upcoming earnings
                if stock['earnings_date']:
                    try:
                        earnings_date = datetime.strptime(stock['earnings_date'], '%Y-%m-%d')
                        days_until_earnings = (earnings_date - today).days
                        if 0 <= days_until_earnings <= EARNINGS_ALERT_DAYS:
                            alerts.append(f"• {stock['ticker']} - Earnings in {days_until_earnings} days ({stock['earnings_date']})")
                    except ValueError:
                        # Invalid date format in database, skip
                        pass
                
                # Check for investigation required status
                if stock['position_status'] == "INVESTIGATION REQUIRED":
                    alerts.append(f"• {stock['ticker']} - Investigation Required")
            
            except (ValueError, TypeError):
                # Skip stocks with invalid data
                pass
        
        if alerts:
            alert_msg = "Alerts:\n\n" + "\n".join(alerts)
            messagebox.showinfo("Alerts", alert_msg)
        else:
            messagebox.showinfo("Alerts", "No alerts at this time.")
    
    def on_stock_double_click(self, event):
        """Handle double-click on stock."""
        self.view_details()


def main():
    """Main entry point."""
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
