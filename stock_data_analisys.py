import random
from tkinter import *
from tkinter import ttk, messagebox
from captcha.image import ImageCaptcha
from openchart import NSEData
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  # Import numpy for regression calculations
import mplcursors  # For interactive hover feature

# Initialize NSEData
nse = NSEData()
nse.download()

# Global variables
captext = ''
lt = ['SBIN', 'HDFC', 'INFY']  # Example stock names for the dropdown

# Sample stock data for testing (date and price values)
dates = [
    "28-01-2025 09:29", "28-01-2025 09:44", "28-01-2025 09:59", 
    "28-01-2025 10:14", "28-01-2025 10:29", "25-02-2025 14:29", 
    "25-02-2025 14:44", "25-02-2025 14:59", "25-02-2025 15:14", "25-02-2025 15:29"
]
open_prices = [350, 360, 355, 365, 370, 420, 430, 440, 450, 460]  # Simulated Open prices
high_prices = [355, 365, 360, 375, 380, 425, 435, 445, 455, 465]  # Simulated High prices

def gen():
    """Generate and display a captcha."""
    img = ImageCaptcha(width=100, height=100)
    a1 = random.random() * 120
    m1 = chr(round(a1))
    a2 = random.random() * 1500
    m2 = round(a2)
    global captext
    captext = str(m1) + str(m2)
    messagebox.showinfo('Hi', captext)
    data = img.generate(captext)
    img.write(captext, 'captchaone.png')
    messagebox.showinfo("hi", "Captcha generated")

def showcap():
    """Show the generated captcha image."""
    try:
        img = PhotoImage(file='C:\\Users\\hyd\\captchaone.png')  # Update with the correct path
        a.configure(image=img)
        a.image = img  # Keep a reference to the image
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load captcha image: {e}")

def login():
    """Handle login with username, password, and captcha."""
    if d.get() == 'test' and f.get() == '123' and h.get() == captext:
        messagebox.showinfo('Hi', 'Success')
        showdash()
        t.withdraw()  # Hide the login window after successful login
    else:
        messagebox.showinfo('Hi', "Failed")

def showdash():
    """Show the dashboard after successful login."""
    tm = Toplevel(t)
    tm.geometry("1000x1000")  # Adjusted for full screen within a reasonable size
    tm.config(bg='#0E4D92')  # Set background color for the dashboard window

    # Dashboard contents with improved colors
    b = Label(tm, text="Stock Analysis", font=("Arial", 24, "bold"), bg='#0E4D92', fg='white')
    b.place(x=350, y=50)

    b = Label(tm, text="Share name", font=("Arial", 12), bg='#0E4D92', fg='white')
    b.place(x=50, y=100)
    e1 = ttk.Combobox(tm)
    e1['values'] = lt
    e1.place(x=150, y=100)

    c = Label(tm, text="Duration (in days)", font=("Arial", 12), bg='#0E4D92', fg='white')
    c.place(x=50, y=150)
    e2 = Spinbox(tm, from_=1, to=31)
    e2.place(x=250, y=150)

    y = Label(tm, text="Interval (e.g., '1d', '15m')", font=("Arial", 12), bg='#0E4D92', fg='white')
    y.place(x=50, y=200)
    e3 = Spinbox(tm, from_=1, to=12)
    e3.place(x=250, y=200)

    # Create a grid of Labels for showing data information
    grid_labels = {}
    for i, label_name in enumerate(['Open Price', 'High Price']):
        grid_labels[label_name] = Label(tm, text=f'{label_name}: ', font=("Arial", 10), bg='#0E4D92', fg='white')
        grid_labels[label_name].place(x=50 + i * 200, y=250)

    def on_show_chart_click():
        """Fetch the stock chart and regression line when the button is clicked."""
        try:
            # Get the values for duration and interval
            duration = int(e2.get())  # Get the duration entered by the user
            interval = e3.get().strip()  # Get the interval entered by the user

            if duration <= 0:
                raise ValueError("Duration should be a positive integer.")
            if not interval:
                raise ValueError("Interval cannot be empty.")
            
            # Here we are using the predefined sample data instead of fetching real stock data
            data_dates = [datetime.datetime.strptime(date, "%d-%m-%Y %H:%M") for date in dates]
            open_prices_data = open_prices
            high_prices_data = high_prices

            # Create a matplotlib figure with two subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))  # Larger figure for better display

            # Bar chart subplot (ax1)
            ax1.bar(data_dates, open_prices_data, color='blue', label='Open Price')
            ax1.set_title('Stock Data', color='yellow')
            ax1.set_xlabel('Date', color='white')
            ax1.set_ylabel('Open Price', color='white')
            ax1.legend()

            # Prepare data for regression (Use Open prices for X and High prices for Y)
            x = np.array(open_prices_data)  # Independent variable (Open Price)
            y = np.array(high_prices_data)  # Dependent variable (High Price)

            # Fit a linear regression line
            coefficients = np.polyfit(x, y, 1)  # Polynomial fit of degree 1 (linear regression)
            poly = np.poly1d(coefficients)

            # Linear regression plot subplot (ax2)
            scatter_plot = ax2.plot(x, y, 'bo', label='Data Points')  # Scatter plot for data points
            x_range = np.linspace(min(x), max(x), 100)
            y_range = poly(x_range)  # Get the regression line
            ax2.plot(x_range, y_range, color='red', label='Regression Line')

            ax2.set_title('Linear Regression', color='yellow')
            ax2.set_xlabel('Open Price', color='white')
            ax2.set_ylabel('High Price', color='white')
            ax2.legend()

            # Use mplcursors to enable hover functionality on the scatter plot
            mplcursors.cursor(scatter_plot, hover=True).connect(
                "add", lambda sel: update_grid_labels(sel.index, x[sel.index], y[sel.index])
            )

            # Embed the plot into the Tkinter window using FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=tm)  # Create a canvas to embed the plot
            canvas.draw()
            canvas.get_tk_widget().place(x=500, y=150)  # Place the plot in the window

            messagebox.showinfo("Success", "Chart displayed with Regression Line!")

            # Store the regression coefficients to use for Buy/Sell logic
            return coefficients[0]  # Return the slope (first coefficient)

        except ValueError as ve:
            messagebox.showerror("Invalid Input", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

    def update_grid_labels(index, open_value, high_value):
        """Update the grid labels with the data information on hover."""
        grid_labels['Open Price'].config(text=f'Open Price: {open_value}')
        grid_labels['High Price'].config(text=f'High Price: {high_value}')

    def on_buy_click():
        """Simulate the Buy action based on regression slope."""
        slope = on_show_chart_click()  # Get the slope from the regression line
        if slope > 0:
            messagebox.showinfo("Action", "It's a good time to BUY!")
        else:
            messagebox.showinfo("Action", "Selling might be a better option.")

    def on_sell_click():
        """Simulate the Sell action based on regression slope."""
        slope = on_show_chart_click()  # Get the slope from the regression line
        if slope < 0:
            messagebox.showinfo("Action", "It's a good time to SELL!")
        else:
            messagebox.showinfo("Action", "Buying might be a better option.")

    # Button to show the chart
    bta = Button(tm, text="Show chart", fg="red", bg="yellow", command=on_show_chart_click)
    bta.place(x=150, y=250)

    # Buy and Sell buttons with colorful styles
    bt_buy = Button(tm, text="Buy", fg="white", bg="green", command=on_buy_click, font=("Arial", 14, "bold"))
    bt_buy.place(x=150, y=500)

    bt_sell = Button(tm, text="Sell", fg="white", bg="red", command=on_sell_click, font=("Arial", 14, "bold"))
    bt_sell.place(x=200, y=500)

def cts():
    """Close the application."""
    t.destroy()  # If you want to quit the program completely, but avoid quitting for re-running

# Main window setup
t = Tk()
t.geometry('500x500')  # Set an initial window size
t.config(bg='#1E3A3A')  # Set the background color of the login screen

# Login screen components
bt1 = Button(t, text="Generate Captcha", command=gen, bg="yellow",fg='#1E3A3A', font=("Arial", 10, "bold"))
bt1.place(x=200, y=50)

bt2 = Button(t, text="Show Captcha", command=showcap, bg="yellow",fg='#1E3A3A', font=("Arial", 10, "bold"))
bt2.place(x=400, y=50)

a = Label(t, text="Captcha", bg='#1E3A3A', fg="white", font=("Arial", 12))
a.place(x=300, y=100)



b = Label(t, text="Login", bg='#1E3A3A', fg="white", font=("Arial", 20, "bold"))
b.place(x=200, y=200)

d = Entry(t, width=20)
d.place(x=450, y=200)

e = Label(t, text="Password", bg='#1E3A3A', fg="white", font=("Arial", 20, "bold"))
e.place(x=200, y=250)

f = Entry(t, width=20, show="*")  # Hide the password input
f.place(x=450, y=250)

g = Label(t, text="Captcha", bg='#1E3A3A', fg="white", font=("Arial", 20, "bold"))
g.place(x=200, y=300)

h = Entry(t, width=20)
h.place(x=450, y=300)

bt3 = Button(t, text="Login", command=login, bg="aqua", fg='#1E3A3A', font=("Arial", 14, "bold"))
bt3.place(x=300, y=350)

bt4 = Button(t, text="Close", command=cts, bg="red", fg='#1E3A3A', font=("Arial", 14, "bold"))
bt4.place(x=400, y=350)

# To reset the window (not to restart the kernel, but just to "reset" the app without closing)
t.mainloop()