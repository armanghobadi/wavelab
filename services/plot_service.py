from tkinter import filedialog, messagebox

class PlotService:
    @staticmethod
    def save_plots(fig):
        filetypes = [
            ('PNG files', '*.png'),
            ('JPEG files', '*.jpg'),
            ('PDF files', '*.pdf'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes,
            title="Save Plots As")
            
        if filename:
            try:
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save plots: {str(e)}")
                return False
        return False