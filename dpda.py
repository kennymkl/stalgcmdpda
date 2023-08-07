# Deterministic Pushdown Automata simulation by 
# Longno, Darren
# Lu, Juhlia
# Villarama, Kenn

# Section S13

# References:
# https://github.com/DorkArn02/python-deterministic-automaton (GUI)


from tkinter import filedialog 
from tkinter import messagebox
import customtkinter as ctk
import os

def open_help():
    messagebox.showinfo("Help", """
    You can make an arbitrary DPDA with this simulator
    Usage:
      1) Enter the name of the DPDA program
      2) Enter symbols for the input alphabet, comma separated (e.g., a,b,c)
      3) Enter symbols for the stack alphabet, comma separated
      4) Enter the names of the states, separated by commas (e.g., q0,q1)
      5) Enter the name of the state that should be considered the start state
      6) Enter state names marked as accepting states, comma separated
      7) Enter transition rules, one per line, in the format: <Initial_State_Name>,<Input_Symbol>,<stack_top>|<New_State_Name>,<new_stack_top>
      8) Use "~" to represent "ε"
    """)



def simulate_dpda(input_str, rules, initial_state, accepting_states, update_status_callback):
    stack = []  # Initialize an empty stack
    current_state = initial_state

    # Simulate the DPDA
    for symbol in input_str:
        # First, follow epsilon rules
        while True:
            epsilon_rule_found = False
            for key, value in rules.items():
                if key[0] == current_state and key[1] == "~":
                    top = key[2]
                    if (len(stack) != 0 and (top == stack[-1] or top == "~")) or (len(stack) == 0 and top == "~"):
                        current_state = value[0]
                        if len(stack) != 0 and top != "~":
                            stack.pop()
                        if value[1] != "~":
                            stack.append(value[1])
                        epsilon_rule_found = True
                        break

            if not epsilon_rule_found:
                break

        # Then, find a matching rule for the transition character
        transition_key = (current_state, symbol, stack[-1] if stack else "~")
        if transition_key in rules:
            new_state, new_stack_top = rules[transition_key]
            current_state = new_state
            if stack and transition_key[2] != '~':  # If not empty symbol, pop from stack
                stack.pop()
            if new_stack_top != '~':  # If not empty symbol, push to stack
                stack.append(new_stack_top)
        else:
            messagebox.showerror("DPDA Simulator", "The DPDA rejected the given input!")
            return

        update_status_callback(f"\nCurrent state: {current_state}, Input symbol: {symbol}, Stack: {stack}")

    if current_state in accepting_states and not stack:
        update_status_callback("\nFINAL STATUS: Accepted")
        messagebox.showinfo("DPDA Simulator", "The DPDA accepted the given input!")
    else:
        update_status_callback("\nFINAL STATUS: Rejected")
        messagebox.showerror("DPDA Simulator", "The DPDA rejected the given input!")

def parse_rules(name, input_alphabet, stack_alphabet, states, initial_state, accepting_states, rules_str, input_str, update_status_callback):
    input_alphabet = input_alphabet.split(',')
    stack_alphabet = stack_alphabet.split(',')
    states = states.split(',')
    accepting_states = accepting_states.split(',')
    rules = [rule.split('|') for rule in rules_str.strip().split('\n') if rule.strip()]

    # Translating the rules into a more accessible format
    transitions = {}
    for rule in rules:
        initial_part = rule[0].split(',')
        new_part = rule[1].split(',')
        key = (initial_part[0].strip(), initial_part[1].strip(), initial_part[2].strip())
        transitions[key] = (new_part[0].strip(), new_part[1].strip())
    
    #print("Parsed transitions:", transitions)

    # Loop over each of the test strings
    for test_str in input_str.splitlines():
        test_str = test_str.strip()
        if not test_str:
            continue

        #print(f"\nTest String: {test_str}")

        # Split the test string into individual characters
        input_chars = list(test_str)

        # Simulate the DPDA for each test string
        simulate_dpda(input_chars, transitions, initial_state, accepting_states,  update_status_callback)
        
class App(ctk.CTk):
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.clear_textboxes()
            file_name = os.path.basename(file_path)
            file_name = os.path.splitext(file_name)[0]
            with open(file_path, 'r') as file:
                content = file.read()
                lines = content.split('\n')
                
                self.dpda_name.delete(0,ctk.END)
                self.dpda_name.insert(0,file_name)
                self.input_alphabet.delete(0, ctk.END)
                self.input_alphabet.insert(0, lines[0])

                self.stack_alphabet.delete(0, ctk.END)
                self.stack_alphabet.insert(0, lines[1])

                self.states.delete(0, ctk.END)
                self.states.insert(0, lines[2])

                self.initial_state.delete(0, ctk.END)
                self.initial_state.insert(0, lines[3])

                self.accepting_states.delete(0, ctk.END)
                self.accepting_states.insert(0, lines[4])

                self.rules.delete("1.0", ctk.END)
                self.rules.insert("1.0", '\n'.join(lines[5:-1]))
     
    def clear_textboxes(self):
        self.dpda_name.delete(0, ctk.END)
        self.input_alphabet.delete(0, ctk.END)
        self.stack_alphabet.delete(0, ctk.END)
        self.states.delete(0, ctk.END)
        self.initial_state.delete(0, ctk.END)
        self.accepting_states.delete(0, ctk.END)
        self.rules.delete("1.0", ctk.END)
        self.input.delete(0, ctk.END)
        
    def update_status(self, message):
        self.status.insert(ctk.END, message + "\n")
        self.status.see(ctk.END)
                
    def save_file(self):
        file_name = self.dpda_name.get()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=file_name, filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.input_alphabet.get() + '\n')
                file.write(self.stack_alphabet.get() + '\n')
                file.write(self.states.get() + '\n')
                file.write(self.initial_state.get() + '\n')
                file.write(self.accepting_states.get() + '\n')
                file.write(self.rules.get("1.0", ctk.END).strip() + '\n')
            self.clear_textboxes()
            messagebox.showinfo("DPDA Simulator", "File saved successfully!")

    def __init__(self):
        ctk.CTk.__init__(self)
        self.title("DPDA Simulator")
        self.geometry("800x800")
        self.resizable(False, True)
        frame = ctk.CTkFrame(master=self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        title = ctk.CTkLabel(master=frame, text="DPDA Simulator", font=('Roboto', 20))
        title.pack(padx=10, pady=10)

        self.dpda_name = ctk.CTkEntry(master=frame, placeholder_text="Name of DPDA program")
        self.dpda_name.pack(padx=10)

        self.input_alphabet = ctk.CTkEntry(master=frame, placeholder_text="Input alphabet (comma separated)")
        self.input_alphabet.pack(padx=10)

        self.stack_alphabet = ctk.CTkEntry(master=frame, placeholder_text="Stack alphabet (comma separated)")
        self.stack_alphabet.pack(padx=10)

        self.states = ctk.CTkEntry(master=frame, placeholder_text="List of states")
        self.states.pack(padx=10)

        self.initial_state = ctk.CTkEntry(master=frame, placeholder_text="Initial state")
        self.initial_state.pack(padx=10)

        self.accepting_states = ctk.CTkEntry(master=frame, placeholder_text="Accepting states")
        self.accepting_states.pack(padx=10)

        self.rules = ctk.CTkTextbox(master=frame, font=('monospace', 17))
        self.rules.pack(padx=10, pady=10)

        self.input = ctk.CTkEntry(master=frame, placeholder_text="Input string")
        self.input.pack(padx=10, pady=10)

        self.load_file_btn = ctk.CTkButton(master=frame, text="Load DPDA", command=self.load_file)
        self.load_file_btn.pack(padx=10, pady=10)

        self.save_file_btn = ctk.CTkButton(master=frame, text="Save DPDA", command=self.save_file)
        self.save_file_btn.pack(padx=10, pady=10)


        btn = ctk.CTkButton(master=frame, text="Start machine", command=lambda: parse_rules(
            self.dpda_name.get(),
            self.input_alphabet.get(),
            self.stack_alphabet.get(),
            self.states.get(),
            self.initial_state.get(),
            self.accepting_states.get(),
            self.rules.get("1.0", ctk.END),
            self.input.get(),
            self.update_status
        ))
        btn.pack(padx=10, pady=10)

        self.help = ctk.CTkButton(master=frame, text="Get help", command=open_help)
        self.help.pack(padx=10, pady=10)

        self.status = ctk.CTkTextbox(master=frame)
        self.status.pack(padx=10, pady=10, fill='both')
        self.status.insert(ctk.END, "[MACHINE LOGS/STEPS]:\n")

        ctk.CTk.mainloop(self)

if __name__ == '__main__':
    app = App()

