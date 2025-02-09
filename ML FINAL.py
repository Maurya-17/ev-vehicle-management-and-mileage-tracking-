import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
import os
import sys

class EVManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EV Vehicle Management System")
        self.root.geometry("800x600")
        
        self.data = []
        if os.path.exists('ev_vehicle_maintenance_mileage_data.csv'):
            self.df = pd.read_csv('ev_vehicle_maintenance_mileage_data.csv')
        else:
            self.df = pd.DataFrame(columns=[
                'Vehicle_ID', 'Make', 'Model', 'Year', 'Battery_Capacity_kWh',
                'Odometer_Reading_km', 'Charge_Level_%', 'Maintenance_Date',
                'Service_Type', 'Service_Cost', 'Energy_Consumption_kWh_per_100km',
                'Estimated_Range_km'
            ])

        self.show_login()

    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        ttk.Label(frame, text="EV Management System Login", font=("Helvetica", 16)).pack(pady=20)

        ttk.Label(frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(pady=5)

        ttk.Label(frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.check_login).pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "maurya" and password == "maurya123":
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        ttk.Label(frame, text="EV Management System", font=("Helvetica", 16)).pack(pady=20)

        ttk.Button(frame, text="Vehicle Registration", command=self.show_vehicle_registration).pack(pady=10, fill='x')
        ttk.Button(frame, text="Maintenance Records", command=self.show_maintenance_form).pack(pady=10, fill='x')
        ttk.Button(frame, text="Mileage Tracking", command=self.show_mileage_tracking).pack(pady=10, fill='x')
        ttk.Button(frame, text="View Analytics", command=self.show_analytics).pack(pady=10, fill='x')
        ttk.Button(frame, text="Clear All Data", command=self.clear_all_data).pack(pady=10, fill='x')  # New button for clearing data
        ttk.Button(frame, text="Logout", command=self.show_login).pack(pady=10, fill='x')

    def show_vehicle_registration(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        ttk.Label(frame, text="Vehicle Registration", font=("Helvetica", 16)).pack(pady=20)

        labels = ['Vehicle ID:', 'Make:', 'Model:', 'Year:']
        self.vehicle_entries = {}

        for label in labels:
            ttk.Label(frame, text=label).pack(pady=5)
            self.vehicle_entries[label] = ttk.Entry(frame)
            self.vehicle_entries[label].pack(pady=5)

        ttk.Button(frame, text="Submit", command=self.save_vehicle_data).pack(pady=20)
        ttk.Button(frame, text="Back to Main Menu", command=self.show_main_menu).pack()

    def show_maintenance_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        ttk.Label(frame, text="Maintenance Record", font=("Helvetica", 16)).pack(pady=20)

        self.maintenance_entries = {}
        fields = [
            'Charge Level (%):', 'Maintenance Date (YYYY-MM-DD):', 
            'Service Type:', 'Service Cost ($):',
            'Energy Consumed (kWh/100 km):', 'Estimated Range (km):'
        ]

        for field in fields:
            ttk.Label(frame, text=field).pack(pady=5)
            self.maintenance_entries[field] = ttk.Entry(frame)
            self.maintenance_entries[field].pack(pady=5)

        ttk.Button(frame, text="Submit", command=self.save_maintenance_data).pack(pady=20)
        ttk.Button(frame, text="Back to Main Menu", command=self.show_main_menu).pack()

    def show_mileage_tracking(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = ttk.Frame(self.root)
        frame.pack(pady=50)

        ttk.Label(frame, text="Mileage Tracking", font=("Helvetica", 16)).pack(pady=20)

        self.mileage_entries = {}
        fields = ['Battery Capacity (kWh):', 'Odometer Reading (km):']

        for field in fields:
            ttk.Label(frame, text=field).pack(pady=5)
            self.mileage_entries[field] = ttk.Entry(frame)
            self.mileage_entries[field].pack(pady=5)

        ttk.Button(frame, text="Submit", command=self.save_mileage_data).pack(pady=20)
        ttk.Button(frame, text="Back to Main Menu", command=self.show_main_menu).pack()

    def show_analytics(self):
        if len(self.df) < 2:
            messagebox.showwarning("Warning", "Not enough data for analysis")
            return

        analytics_window = tk.Toplevel(self.root)
        analytics_window.title("EV Analytics")
        analytics_window.geometry("1000x800")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

        sns.scatterplot(data=self.df, x='Battery_Capacity_kWh', y='Odometer_Reading_km', ax=ax1)
        ax1.set_title('Battery Capacity vs Odometer Reading')
        ax1.set_xlabel('Battery Capacity (kWh)')
        ax1.set_ylabel('Odometer Reading (km)')

        sns.scatterplot(data=self.df, x='Charge_Level_%', y='Energy_Consumption_kWh_per_100km', ax=ax2)
        ax2.set_title('Charge Level vs Energy Consumption')
        ax2.set_xlabel('Charge Level (%)')
        ax2.set_ylabel('Energy Consumption (kWh per 100 km)')

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        canvas = FigureCanvasTkAgg(fig, master=analytics_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        ttk.Button(analytics_window, text="Close", command=analytics_window.destroy).pack(pady=10)

    def save_vehicle_data(self):
        try:
            new_data = {
                'Vehicle_ID': self.vehicle_entries['Vehicle ID:'].get(),
                'Make': self.vehicle_entries['Make:'].get(),
                'Model': self.vehicle_entries['Model:'].get(),
                'Year': int(self.vehicle_entries['Year:'].get())
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
            self.save_to_csv()
            messagebox.showinfo("Success", "Vehicle data saved successfully")
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def save_maintenance_data(self):
        try:
            new_data = {
                'Charge_Level_%': float(self.maintenance_entries['Charge Level (%):'].get()),
                'Maintenance_Date': self.maintenance_entries['Maintenance Date (YYYY-MM-DD):'].get(),
                'Service_Type': self.maintenance_entries['Service Type:'].get(),
                'Service_Cost': float(self.maintenance_entries['Service Cost ($):'].get()),
                'Energy_Consumption_kWh_per_100km': float(self.maintenance_entries['Energy Consumed (kWh/100 km):'].get()),
                'Estimated_Range_km': float(self.maintenance_entries['Estimated Range (km):'].get())
            }
            if not (0 <= new_data['Charge_Level_%'] <= 100):
                raise ValueError("Charge level must be between 0 and 100")
            
            self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
            self.save_to_csv()
            messagebox.showinfo("Success", "Maintenance data saved successfully")
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")

    def save_mileage_data(self):
        try:
            new_data = {
                'Battery_Capacity_kWh': float(self.mileage_entries['Battery Capacity (kWh):'].get()),
                'Odometer_Reading_km': float(self.mileage_entries['Odometer Reading (km):'].get())
        }
        
        # Check if the vehicle needs service
            if new_data['Odometer_Reading_km'] / new_data['Battery_Capacity_kWh'] > 1000:
                messagebox.showinfo("Service Status", "Vehicle needs service")
            else:
                messagebox.showinfo("Service Status", "Vehicle is good to go for a few more months")
        
            self.df = pd.concat([self.df, pd.DataFrame([new_data])], ignore_index=True)
            self.save_to_csv()
            messagebox.showinfo("Success", "Mileage data saved successfully")
            self.show_main_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")


    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data?"):
            self.df = pd.DataFrame(columns=self.df.columns)  # Clear all data
            self.save_to_csv()
            messagebox.showinfo("Success", "All data cleared successfully")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                self.save_to_csv()
                plt.close('all') 
                self.root.destroy()
                sys.exit(0)
            except Exception as e:
                messagebox.showerror("Error", f"Error while closing: {str(e)}")
                sys.exit(1)

    def on_interrupt(self, event):
        self.on_closing()

    def save_to_csv(self):
        try:
            self.df.to_csv('ev_vehicle_maintenance_mileage_data.csv', index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.on_closing()

if __name__ == "__main__":
    try:
        app = EVManagementSystem()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {str(e)}")
        sys.exit(1)
