# NOTE: Any theme called default will be the default theme.

import argparse
from datetime import datetime
from json import dump, load
from tkinter import *
from tkinter import colorchooser, messagebox, simpledialog
from hass import *
try:
    import tkfontchooser
except:
    os.system("python -m pip install tkfontchooser")
    import tkfontchooser
try:
    import tkcalendar
except:
    os.system("python -m pip install tkcalendar")
    import tkcalendar

class Countdown:
    """Countdown clock"""
    def __init__(self, infile = 'hass', outfile = 'hass'):
        self.root = Tk()
        self.root.title("Countdown")
        self.root.withdraw()
        self.root.iconbitmap(default="Clock.ico")
        self.infile = infile
        self.outfile = outfile #The JSON file to get data from
        self.load_data()
        #self.root.configure(bg = self.background_color)
        self.root.state('zoomed')
        self.add_event_button = Button(self.root, text = "New event", command = self.add_event, relief = 'flat', cursor = 'hand2')
        self.add_event_button.grid(row = 0)
        self.remove_event_button = Button(self.root, text = "Remove event", command = self.remove_event, relief = 'flat', cursor = 'hand2')
        self.remove_event_button.grid(row = 0, column = 1)
        self.add_theme_button = Button(self.root, text = "Add theme", command = self.add_theme, relief = 'flat', cursor = 'hand2')
        self.add_theme_button.grid(row = 0, column = 2)
        self.load_theme_button = Button(self.root, text = "Load theme", command = self.load_theme, relief = 'flat', cursor = 'hand2')
        self.load_theme_button.grid(row = 0, column = 3)
        self.remove_theme_button = Button(self.root, text = "Remove theme", command = self.remove_theme, relief = 'flat', cursor = 'hand2')
        self.remove_theme_button.grid(row = 0, column = 4)
        self.canvas = Canvas(self.root, bd = 0, width = self.root.winfo_screenwidth(), height = self.root.winfo_screenheight() - 50, highlightthickness=0)
        self.canvas.grid(row = 2, columnspan = 20)
        self.label = Label(self.root, width = 10, height = 1, anchor = 'w', text = 'Countdown')
        self.label.grid(row = 1)
        self.load_theme(self.current_theme)
        self.update()

    def load_data(self):
        """Loads data from JSON"""
        if self.infile == "hass":
            try:
                data = get_state("sensor.countdown_data")["attributes"]["countdown_data"]["countdown_data"]
                print(data)
            except Exception as e:
                print(e)
                data = {'events':{},'themes':{}, 'current_theme': 'Default'}
        else:
            try:
                with open(self.infile) as file:
                    data = load(file)
            except:
                data = {'events':{},'themes':{}, 'current_theme': 'Default'}
        try:
            assert data["themes"] != None
        except (KeyError, AssertionError):
            self.themes = {}
            data["themes"] = {}
        try:
            assert data["events"] != None
        except (KeyError, AssertionError):
            self.events = {}
            data["events"] = {}
        try:
            self.themes = data["themes"]
            assert data["themes"]["Default"] != None
        except (KeyError, AssertionError):
            self.themes["Default"] = {
                "background": "#000000",
                "heading": "#0000ff",
                "event": "#bb0000",
                "soon": "#e8e800",
                "today": "#00df70",
                "font": {
                    "family": "Courier New",
                    "size": 20,
                    "weight": "normal",
                    "slant": "roman",
                    "underline": 0,
                    "overstrike": 0
                },
                "space": 25
            }
        try:
            self.current_theme = data["current_theme"]
            assert self.themes[self.current_theme] != None
        except KeyError:
            self.current_theme = "Default"
        self.events = {}
        for key, value in data["events"].items():
            self.events[key] = datetime.fromisoformat(value)
        self.sort_events()
        self.infile = self.outfile
        self.save_data()

    def sort_events(self):
        self.events = dict(sorted(self.events.items(), key=lambda x:x[1]))
        self.save_data()

    def time_until(self, title, event):
        """Return a list with the time until an event"""
        now = datetime.now()
        until = event - now
        days = until.days
        seconds = until.seconds % 60
        hours = until.seconds // 3600
        minutes = until.seconds // 60 % 60
        strdays = str(days) + (" day," if days == 1 else " days,")
        strseconds = str(seconds) + (" second." if seconds == 1 else " seconds.")
        strhours = str(hours) + (" hour," if hours == 1 else " hours,")
        strminutes = str(minutes) + (" minute," if minutes == 1 else " minutes,")
        message = '%s is in %s %s %s and %s' % (title, strdays, strhours, strminutes, strseconds)
        return [message, days, hours, minutes, seconds]

    def update(self):
        """Update the canvas (called every second)"""
        y = int(self.font[1]) + 10
        past_events = []
        self.canvas.delete("event")
        for title, event in self.events.items():
            until = self.time_until(title, event)
            if until[1] in range(1, 7):
                color = self.soon_color
            elif until[1] < 0:
                messagebox.showinfo(title, title + " happened.")
                past_events.append(title)
                continue
            elif until[1] == 0:
                color = self.today_color
            else:
                color = self.event_color
            self.canvas.create_text(5, y, anchor = 'w', \
                    fill = color, font = self.font, \
                    text = until[0], tags = "event")
            y += self.vertical_space
        for title in past_events:
            self.remove_event(title)
            
        self.root.after(1000, self.update)
        
    def remove_event(self, event=None):
        """Removes an event from the file"""
        if not event:
            event = self.show_radio_dialog("Select event to remove", self.events.keys(), current_state = list(self.events.keys())[0])
        if not event:
            return
        del self.events[event]
        self.save_data()

    def get_datetime(self, submit_button_name = "OK", cancel_button_name = "Cancel"):
        stringvar = StringVar(self.root)
        date_picker = DatePicker(self.root, submit_button_name, cancel_button_name)
        self.root.wait_window(date_picker.root)
        #print(date_picker.data)
        return date_picker.data

    def add_event(self):
        """Add an event to the list"""
        #event_time = datetime.now()
        name = simpledialog.askstring("Name", "Name of event")
        while name == "":
            messagebox.showerror("Error", "Name must not be blank.")
            name = simpledialog.askstring("Name", "Name of event")
        if name in self.events.keys():
            if not messagebox.askyesno("Event exists", "'{name}' already exists! Do you want to edit it?"):
                return
        if name == None:
            return
        event_datetime = self.get_datetime()
        if event_datetime:
            self.load_data()
            self.events[name] = event_datetime
        else:
            return
        self.sort_events()
        self.save_data()
    
    def save_data(self):
        data = {"themes": self.themes, "events": {}, "current_theme": self.current_theme}
        for key, value in self.events.items():
            data["events"][key] = datetime.isoformat(value)
        if self.outfile == "hass":
            print(data)
            call_service("script.countdown_data", data = {"countdown_data": data})
        else:
            with open(self.outfile, "w+") as data_file:
                dump(data, data_file, indent=2)

    def remove_theme(self, name = None):
        """Deletes a theme"""
        if not name:
            name = self.show_radio_dialog("Select a theme.", self.themes.keys(), list(self.themes.keys())[0])
            if not name:
                return
            else:
                name = name.title()
        else:
            name = name.title()
        if name in self.themes.keys():
            del self.themes[name]
        else:
            messagebox.showerror("Error", "Invalid theme")
        self.save_data()

    def load_theme(self, name = None):
        """Loads a theme from data"""
        if not name:
            name = self.show_radio_dialog("Select a theme.", self.themes.keys(), self.current_theme)
            if not name:
                return
            name = name.title()
        else:
            name = name.title()
        try:
            theme = self.themes[name]
        except:
            messagebox.showerror("Error", "Invalid theme")
            return
        self.current_theme = name
        self.background_color = theme['background']
        self.heading_color = theme['heading']
        self.event_color = theme['event']
        self.vertical_space = theme['space']
        font_family = theme['font']['family']
        font_size = str(theme['font']['size'])
        font_weight = theme['font']['weight']
        font_slant = theme['font']['slant']
        font_underline = ' underline' if theme['font']['underline'] == 1 else ''
        font_overstrike = ' overstrike' if theme['font']['overstrike'] == 1 else ''
        self.font = (font_family, font_size, font_weight + ' ' + font_slant + font_underline + font_overstrike)
        self.soon_color = theme['soon']
        self.today_color = theme['today']
        for b in [self.add_event_button, self.remove_event_button, self.add_theme_button, self.load_theme_button, self.remove_theme_button]:
            b.configure(bg = self.background_color, font = self.font, fg = self.heading_color)
        self.canvas.itemconfig("event", fill = self.heading_color, font = self.font)
        self.canvas.configure(bg = self.background_color)
        self.root.configure(bg = self.background_color)
        self.label.configure(fg = self.heading_color, bg = self.background_color,
                             font = (self.font[0], str(int(self.font[1]) + 10), self.font[2]))
        self.save_data()
    
    def show_radio_dialog(self, title, items, current_state = "", submit_button_name = "OK", cancel_button_name = "Cancel"):
        stringvar = StringVar(self.root)
        radio_dialog = RadioButtonDialog(self.root, title, items, stringvar, current_state, submit_button_name, cancel_button_name)
        self.root.wait_window(radio_dialog.root)
        #print(stringvar.get())
        return stringvar.get()

    def add_theme(self):
        """Creates theme from user input"""
        t = {}
        name = simpledialog.askstring("Name", "Name of the theme")
        if not name:
            return
        name = name.title()
        if name in self.themes.keys():
            if not messagebox.askyesno("Theme exists", f"'{name}' already exists! Do you want to edit it?"):
                return
        t['background'] = colorchooser.askcolor(title = "Background color")[1]
        if not t['background']:
            return
        t['heading'] = colorchooser.askcolor(title = "Heading color")[1]
        if not t['heading']:
            return
        t['event'] = colorchooser.askcolor(title = "Event color")[1]
        if not t['event']:
            return
        t['soon'] = colorchooser.askcolor(title = "Soon event color")[1]
        if not t['soon']:
            return
        t['today'] = colorchooser.askcolor(title = "Today event color")[1]
        if not t['today']:
            return
        t['font'] = tkfontchooser.askfont(title = "Font")
        if not t['font']:
            return
        t['space'] = simpledialog.askinteger("Spacing", "Line spacing\n(should be greater than font size)")
        if not t['space']:
            return
        self.load_data()
        self.themes[name] = t
        self.save_data()
        self.load_theme(name)

class RadioButtonDialog:
    def __init__(self, parent, title, items, stringvar, current_state = "", submit_button_name = "Submit", cancel_button_name = "Cancel"):
        if parent:
            self.root = Toplevel(parent)
            self.root.grab_set()
        else:
            self.root = Tk()
        self.root.title(title)
        self.radio_buttons = []
        self.stringvar = stringvar
        self.stringvar.set(current_state)
        for button_name in items:
            new_button = Radiobutton(self.root, text = button_name, value = button_name, variable = self.stringvar)
            new_button.pack()
            self.radio_buttons.append(new_button)
        self.button_frame = Frame(self.root)
        self.button_frame.pack()
        self.cancel_button = Button(self.button_frame, text=cancel_button_name, command=self.cancel)
        self.cancel_button.grid(row=0, column=0)
        self.submit_button = Button(self.button_frame, text = submit_button_name, command = self.root.destroy)
        self.submit_button.grid(row=0, column=1)
    def cancel(self):
        self.stringvar.set("")
        self.root.destroy()

class DatePicker(): 
    def __init__(self, parent, submit_button_name = "OK", cancel_button_name = "Cancel"):
        if parent:
            self.root = Toplevel(parent)
            self.root.grab_set()
        else:
            self.root = Tk()
        self.data = None
        self.root.title("Choose a date.")
        self.title_var = StringVar(self.root)
        self.entry = Entry(self.root, textvariable=self.title_var)
        self.calendar = tkcalendar.Calendar(self.root, firstweekday = "sunday")
        self.calendar.pack()
        self.button_frame = Frame(self.root)
        self.button_frame.pack()
        self.hour_var = IntVar(self.root, 12)
        self.minute_var = IntVar(self.root, 0)
        self.second_var = IntVar(self.root, 0)
        self.am_pm_var = StringVar(self.root)
        self.am_pm_var.set("AM")
        self.hour_spinner = Spinbox(self.button_frame, text="Hour", from_ = 1, to = 12, wrap = True, increment = 1, textvariable=self.hour_var)
        self.minute_spinner = Spinbox(self.button_frame, text = "Minute", from_ = 0, to = 59, wrap = True, increment = 1, textvariable=self.minute_var)
        self.second_spinner = Spinbox(self.button_frame, text = "Second", from_ = 0, to = 59, wrap = True, increment = 1, textvariable=self.second_var)
        self.am_pm_menu = OptionMenu(self.button_frame, self.am_pm_var, "AM", "PM")
        self.hour_spinner.grid(row=0, column=0)
        self.minute_spinner.grid(row=0, column=1)
        self.second_spinner.grid(row=0, column=2)
        self.am_pm_menu.grid(row=0, column=3)
        self.cancel_button = Button(self.button_frame, text=cancel_button_name, command=self.cancel)
        self.cancel_button.grid(row=1, column=1)
        self.submit_button = Button(self.button_frame, text = submit_button_name, command = self.submit)
        self.submit_button.grid(row=1, column=2)
    def cancel(self):
        self.data = None
        self.root.destroy()
    def submit(self):
        hour = str(self.hour_var.get()).zfill(2)
        minute = str(self.minute_var.get()).zfill(2)
        second = str(self.second_var.get()).zfill(2)
        am_pm = str(self.am_pm_var.get()).zfill(2)
        string_time = hour + ":" + minute + ":" + second + " " + am_pm
        try:
            event_time = datetime.strptime(string_time, "%I:%M:%S %p")
            event_date = datetime.strptime(self.calendar.get_date(), "%m/%d/%y")
            self.data = [self.title_var.get(), event_time]
            event_datetime = datetime.combine(event_date.date(), event_time.time())
            self.data = event_datetime
        except:
            messagebox.showerror("Error", "Invalid date/time")
            self.data = None
        self.root.destroy()

argparser = argparse.ArgumentParser(prog = "Countdown", description = "Shows the remaining time until user-specified events", add_help = True)
argparser.add_argument("-i", "--infile", type=str, help="The file to load data from initally (default: hass), after first load, loads from --outfile.")
argparser.add_argument("-o", "--outfile", type=str, help="The file to write data to (default: hass)")

args = argparser.parse_args()
if args.infile:
    infile = args.infile
else:
    infile = "hass"
if args.outfile:
    outfile = args.outfile
else:
    outfile = "hass"


if __name__ == "__main__":
    c = Countdown(infile = infile, outfile = outfile)
    c.root.mainloop()
