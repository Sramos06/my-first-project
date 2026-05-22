import tkinter as tk
from tkinter import ttk, messagebox

# --- Functions ---

# Global variable to track the current theme state
is_dark_mode = False

def toggle_theme():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    
    # Define the two color palettes
    if is_dark_mode:
        app_bg = "#1E272E"        
        text_fg = "#D2DAE2"       
        title_fg = "#4BCFFA"      
        total_bg = "#2C3A47"      
        theme_btn_bg = "#F39C12"  
        util_bg = "#8E44AD"       
    else:
        app_bg = "#F4F6F9"        
        text_fg = "#2C3E50"       
        title_fg = "#00509E"      
        total_bg = "#D6EAF8"     
        theme_btn_bg = "#34495E" 
        util_bg = "#9B59B6"       

    # Update main window
    frame.configure(background=app_bg)
    
    # Update all Frames 
    frames = [f_name, f_units, f_year, f_fees, f_fee1, f_fee2, f_fee3, 
              f_scholar_lbl, f_scholar, f_total, f_buttons, f_buttons_extra]
    for f in frames:
        f.configure(background=app_bg)
        
    # Update standard Labels
    standard_labels = [l_student_name, l_units, l_year]
    for l in standard_labels:
        l.configure(background=app_bg, foreground=text_fg)
        
    # Update Header Labels
    header_labels = [l_main_title, l_fees, l_scholar, l_total]
    for hl in header_labels:
        hl.configure(background=app_bg, foreground=title_fg)
        
    # Update Checkbuttons and Radiobuttons
    buttons = [c_lab, c_council, c_reg, c_id, c_cat, c_misc, r_non, r_full, r_partial]
    for btn in buttons:
        btn.configure(background=app_bg, foreground=text_fg, activebackground=app_bg, 
                      activeforeground=text_fg, selectcolor=app_bg)
        
    # Update the Total Entry box and Theme Button
    e_total.configure(background=total_bg, foreground=text_fg)
    b_theme.configure(background=theme_btn_bg)
    
    # Update new extra buttons
    b_receipt.configure(background=util_bg)
    b_save.configure(background=util_bg)
    b_help.configure(background=util_bg)

def show_receipt():
    name = e_name.get()
    total = e_total.get()
    
    if not total:
        messagebox.showwarning("Oops", "Please hit COMPUTE first to generate a receipt!")
        return

    receipt_text = f"--- OFFICIAL RECEIPT ---\n\n"
    receipt_text += f"Student: {name}\n"
    receipt_text += f"Year Level: {cb_year.get()}\n"
    receipt_text += f"Scholarship: {var_scholar.get()}\n\n"
    receipt_text += f"FINAL AMOUNT DUE: {total}\n"
    receipt_text += f"\nThank you for enrolling!"

    messagebox.showinfo("Detailed Receipt", receipt_text)

def save_data():
    name = e_name.get()
    total = e_total.get()
    
    if not name or not total:
        messagebox.showerror("Error", "Please enter a name and compute the fee first.")
        return
        
    with open("student_records.txt", "a") as file:
        file.write(f"Student: {name} | Year: {cb_year.get()} | Amount Due: {total}\n")
        
    messagebox.showinfo("Success", f"Saved record for {name} to 'student_records.txt'!")

def show_help():
    help_text = "How to use this calculator:\n\n"
    help_text += "1. Enter your Name and Units (must be a positive number).\n"
    help_text += "2. Select your Year Level from the dropdown.\n"
    help_text += "3. Check any extra fees that apply.\n"
    help_text += "4. Select your scholarship status.\n"
    help_text += "5. Click COMPUTE to get your total!\n"
    help_text += "6. Use RECEIPT to view details or SAVE to log the file."
    
    messagebox.showinfo("Help / Instructions", help_text)

def compute():
    # VIII. Validate Units Enrolled (Must be positive integer)
    try:
        units = int(e_units.get())
        if units <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please input a correct positive integer value for Units Enrolled.")
        return
    
    # VIII. Validate Year Level (Must not be blank)
    year_level = cb_year.get().strip() 
    if not year_level:
        messagebox.showerror("Error", "Please choose a correct Year Level.")
        return

    # VI. Calculate Year Level Fee based on selection
    year_fees = {
        "1st Year": 100,
        "2nd Year": 200,
        "3rd Year": 300,
        "4th Year": 400,
        "5th Year": 500
    }
    year_fee = year_fees.get(year_level, 0)

    # VI. Calculate Other Fees based on checked items
    other_fees = 0
    if var_lab.get(): other_fees += 200
    if var_reg.get(): other_fees += 50
    if var_cat.get(): other_fees += 50
    if var_council.get(): other_fees += 50
    if var_id.get(): other_fees += 50
    if var_misc.get(): other_fees += 100

    # Base Total calculation
    base_total = (units * 10) + other_fees + year_fee

    # VI. Apply Scholarship Grants logic
    scholar_type = var_scholar.get()
    if scholar_type == "Full Scholar":
        total_amount = 0
    elif scholar_type == "Partial Scholar":
        total_amount = base_total / 2
    else: # Non-Scholar
        total_amount = base_total

    # Display Total Amount in the read-only textbox
    e_total.config(state="normal") 
    e_total.delete(0, tk.END)
    e_total.insert(0, f"P {total_amount:,.2f}") 
    e_total.config(state="readonly") 

def clear():
    # VII. Set the form back to its default values
    e_name.delete(0, tk.END)
    e_units.delete(0, tk.END)
    cb_year.set('') 
    
    # Uncheck all other fees
    var_lab.set(0)
    var_reg.set(0)
    var_cat.set(0)
    var_council.set(0)
    var_id.set(0)
    var_misc.set(0)

    # Default radio button to Non-Scholar
    var_scholar.set("Non-Scholar")

    # Clear total amount box
    e_total.config(state="normal")
    e_total.delete(0, tk.END)
    e_total.config(state="readonly")


# --- Main GUI Setup ---
frame = tk.Tk()
frame.title("Student Fee Calculator")
frame.geometry("480x620") 

# --- Font & Initial Color Styles ---
title_font = ('Arial', 14, 'bold')
header_font = ('Arial', 11, 'bold')
std_font = ('Arial', 10)

app_bg = "#F4F6F9"        
text_fg = "#2C3E50"       
title_fg = "#00509E"      
btn_comp_bg = "#27AE60"   
btn_clear_bg = "#E74C3C"  
total_bg = "#D6EAF8"      
util_bg = "#9B59B6" 

# Apply background color to main window
frame.configure(background=app_bg)

# Variables
var_lab = tk.IntVar()
var_reg = tk.IntVar()
var_cat = tk.IntVar()
var_council = tk.IntVar()
var_id = tk.IntVar()
var_misc = tk.IntVar()
var_scholar = tk.StringVar(value="Non-Scholar") 

# --- Declarations ---

# Main App Title
l_main_title = tk.Label(frame, text="STUDENT FEE CALCULATOR", 
                        font=title_font, foreground=title_fg, background=app_bg)

# Row 0: Student Name 
f_name = tk.Frame(frame, background=app_bg)
l_student_name = tk.Label(f_name, text="Student Name:", width=18, anchor="w", 
                          font=std_font, foreground=text_fg, background=app_bg)
e_name = tk.Entry(f_name, width=32, bd=3, font=std_font) 

# Row 1: Units Enrolled
f_units = tk.Frame(frame, background=app_bg)
l_units = tk.Label(f_units, text="Units Enrolled:", width=18, anchor="w", 
                   font=std_font, foreground=text_fg, background=app_bg)
e_units = tk.Entry(f_units, width=32, bd=3, font=std_font)

# Row 2: Year Level
f_year = tk.Frame(frame, background=app_bg)
l_year = tk.Label(f_year, text="Year Level:", width=18, anchor="w", 
                  font=std_font, foreground=text_fg, background=app_bg)
year_levels = ["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"]
cb_year = ttk.Combobox(f_year, values=year_levels, state="readonly", width=30, font=std_font)
cb_year.set('') 

# Row 3 to 6: Other Fees
f_fees = tk.Frame(frame, background=app_bg)
l_fees = tk.Label(f_fees, text="Other Fees:", width=18, anchor="w", 
                  font=header_font, foreground=title_fg, background=app_bg)

f_fee1 = tk.Frame(frame, background=app_bg)
c_lab = tk.Checkbutton(f_fee1, text="Laboratory Fee (P200)", variable=var_lab, width=22, anchor="w", 
                       font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)
c_council = tk.Checkbutton(f_fee1, text="Student Council (P50)", variable=var_council, width=22, anchor="w", 
                           font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)

f_fee2 = tk.Frame(frame, background=app_bg)
c_reg = tk.Checkbutton(f_fee2, text="Registration Card (P50)", variable=var_reg, width=22, anchor="w", 
                       font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)
c_id = tk.Checkbutton(f_fee2, text="Student ID (P50)", variable=var_id, width=22, anchor="w", 
                      font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)

f_fee3 = tk.Frame(frame, background=app_bg)
c_cat = tk.Checkbutton(f_fee3, text="Catalyst (P50)", variable=var_cat, width=22, anchor="w", 
                       font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)
c_misc = tk.Checkbutton(f_fee3, text="Other Misc (P100)", variable=var_misc, width=22, anchor="w", 
                        font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)

# Row 7 to 9: Scholarship Grants
f_scholar_lbl = tk.Frame(frame, background=app_bg)
l_scholar = tk.Label(f_scholar_lbl, text="Scholarship Grants:", width=18, anchor="w", 
                     font=header_font, foreground=title_fg, background=app_bg)

f_scholar = tk.Frame(frame, background=app_bg)
r_non = tk.Radiobutton(f_scholar, text="Non-Scholar", variable=var_scholar, value="Non-Scholar", 
                               font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)
r_full = tk.Radiobutton(f_scholar, text="Full Scholar", variable=var_scholar, value="Full Scholar",
                                font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)
r_partial = tk.Radiobutton(f_scholar, text="Partial Scholar", variable=var_scholar, value="Partial Scholar", 
                                   font=std_font, foreground=text_fg, background=app_bg, activebackground=app_bg, selectcolor=app_bg)

# Row 10: Total Amount
f_total = tk.Frame(frame, background=app_bg)
l_total = tk.Label(f_total, text="Total Amount:", width=18, anchor="w", 
                   font=header_font, foreground=title_fg, background=app_bg)
e_total = tk.Entry(f_total, width=32, state="readonly", bd=3, 
                   font=title_font, background=total_bg, foreground=text_fg) 

# Row 11: Main Buttons
f_buttons = tk.Frame(frame, background=app_bg)
b_compute = tk.Button(f_buttons, text="COMPUTE", width=12, bd=3, 
                      font=header_font, foreground="white", background=btn_comp_bg, command=compute)
b_clear = tk.Button(f_buttons, text="CLEAR", width=10, bd=3, 
                    font=header_font, foreground="white", background=btn_clear_bg, command=clear)
# Row 11: Extra Features Buttons
b_theme = tk.Button(f_buttons, text="🌗 THEME", width=10, bd=3, 
                    font=header_font, foreground="white", background="#34495E", command=toggle_theme)

# Row 12: Extra Features Buttons
f_buttons_extra = tk.Frame(frame, background=app_bg)
b_receipt = tk.Button(f_buttons_extra, text="🧾 RECEIPT", width=12, bd=3, 
                      font=header_font, foreground="white", background=util_bg, command=show_receipt)
b_save = tk.Button(f_buttons_extra, text="💾 SAVE", width=10, bd=3, 
                   font=header_font, foreground="white", background=util_bg, command=save_data)
b_help = tk.Button(f_buttons_extra, text="❓ HELP", width=10, bd=3, 
                   font=header_font, foreground="white", background=util_bg, command=show_help)

# --- Layout ---

l_main_title.pack(pady=(15, 15))

f_name.pack(anchor="w", padx=20, pady=5)
l_student_name.pack(side="left")
e_name.pack(side="left")

f_units.pack(anchor="w", padx=20, pady=5)
l_units.pack(side="left")
e_units.pack(side="left")

f_year.pack(anchor="w", padx=20, pady=5)
l_year.pack(side="left")
cb_year.pack(side="left")

f_fees.pack(anchor="w", padx=20, pady=(15, 5))
l_fees.pack(side="left")

f_fee1.pack(anchor="w", padx=40)
c_lab.pack(side="left")
c_council.pack(side="left")

f_fee2.pack(anchor="w", padx=40)
c_reg.pack(side="left")
c_id.pack(side="left")

f_fee3.pack(anchor="w", padx=40)
c_cat.pack(side="left")
c_misc.pack(side="left")

f_scholar_lbl.pack(anchor="w", padx=20, pady=(15, 5))
l_scholar.pack(side="left")

f_scholar.pack(anchor="w", padx=40)
r_non.pack(anchor="w", pady=2)
r_full.pack(anchor="w", pady=2)
r_partial.pack(anchor="w", pady=2)

f_total.pack(anchor="w", padx=20, pady=20)
l_total.pack(side="left")
e_total.pack(side="left")

f_buttons.pack(pady=(10, 5))
b_compute.pack(side="left", padx=10)
b_clear.pack(side="left", padx=10)
b_theme.pack(side="left", padx=10) 

f_buttons_extra.pack(pady=(5, 20))
b_receipt.pack(side="left", padx=10)
b_save.pack(side="left", padx=10)
b_help.pack(side="left", padx=10)

# Run the application
frame.mainloop()
