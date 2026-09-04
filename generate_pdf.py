from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Sky Auto Services LLC - Quote Calculator Engine", border=False, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("helvetica", "I", 10)
        self.cell(0, 10, "Architecture & Pricing Engine Documentation", border=False, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("helvetica", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("helvetica", "", 11)
        self.multi_cell(0, 6, body)
        self.ln(5)

pdf = PDF()
pdf.add_page()

pdf.chapter_title("1. Architectural Overview")
pdf.chapter_body(
    "The Sky Auto Services Quote Calculator has been completely overhauled to ensure absolute mathematical precision. "
    "The frontend (built with Next.js/React) handles addressing and converts user-typed cities or zip codes into exact geographic coordinates. "
    "The backend pricing engine (calculate_quote.php) intercepts these coordinates and communicates with a routing engine to determine exact driving distances."
)

pdf.chapter_title("2. Distance Calculation (OSRM Integration)")
pdf.chapter_body(
    "Instead of straight-line 'as the crow flies' estimates, the backend uses the Open Source Routing Machine (OSRM) to calculate true driving distances across the US road network. "
    "In the rare event that the routing server is temporarily unavailable, the system safely falls back to a mathematical Haversine calculation adjusted with a 1.18x real-world curve multiplier, ensuring quotes are never interrupted."
)

pdf.chapter_title("3. The Pricing Algorithm")
pdf.chapter_body(
    "The base cost of transport is calculated dynamically using the following state-specific per-mile base rates:\n\n"
    "- Florida (Snowbird): $0.85/mile\n"
    "- California (Hub): $0.90/mile\n"
    "- Colorado (Standard): $1.10/mile\n"
    "- Wyoming (Rural): $1.45/mile\n"
    "- Montana (Rural): $1.50/mile\n"
    "- Default (Unlisted States): $1.15/mile\n\n"
    "The final base rate applied is the mathematical average of the Origin state's rate and the Destination state's rate."
)

pdf.chapter_title("4. Long-Distance Discounts")
pdf.chapter_body(
    "Because long cross-country hauls cost less per mile to operate, a distance discount multiplier is applied automatically:\n\n"
    "- 0 - 500 Miles: Standard Base Rate (1.00x)\n"
    "- 501 - 1,000 Miles: 15% Discount (0.85x multiplier)\n"
    "- 1,001 - 2,000 Miles: 25% Discount (0.75x multiplier)\n"
    "- Over 2,000 Miles: 35% Discount (0.65x multiplier)\n\n"
    "Route type modifiers also adjust the rate: Hub-to-Hub receives a 10% discount, while Rural-to-Rural incurs a 25% surcharge."
)

pdf.chapter_title("5. Seasonal Surcharges")
pdf.chapter_body(
    "The algorithm automatically applies seasonal price fluctuations based on supply and demand:\n\n"
    "- Snowbird Southbound (Oct-Dec): 20% Surcharge for routes heading into Snowbird states (FL, AZ, NV, TX, etc.).\n"
    "- Snowbird Northbound (Apr-May): 18% Surcharge for routes heading out of Snowbird states.\n"
    "- Winter Northern Routes (Dec-Feb): 10% Surcharge for routes involving northern/winter states."
)

pdf.chapter_title("6. Vehicle & Transport Modifications")
pdf.chapter_body(
    "After the base route cost is calculated, vehicle-specific additions are applied. Small SUVs and EVs add $100. "
    "Large SUVs and 1/2 Ton Pickups add $150. Heavy-Duty Pickups and Minivans add $200. "
    "Heavy Commercial Trucks add $300. Inoperable vehicles receive a flat $150 surcharge.\n\n"
    "Finally, the total base cost is multiplied based on the chosen transport type:\n"
    "- Open Carrier (Standard): 1.00x Multiplier (Minimum $250)\n"
    "- Enclosed (Standard): 1.40x Multiplier (Minimum $450)\n"
    "- Enclosed (Shielded/Liftgate): 1.60x Multiplier (Minimum $650)\n"
    "- Open (Express/Expedited): 1.90x Multiplier (Minimum $850)\n\n"
    "High-value vehicles see an additional premium (15% for $50k-$100k, 30% for over $100k) applied after all transport multipliers."
)

pdf.chapter_title("7. Final Output")
pdf.chapter_body(
    "The engine outputs a precise 'Mid Price' rounded to the nearest $5, with a +/- 10% buffer generating a realistic price range. "
    "Transit time (ETA) is also automatically calculated based on approximately 450 driving miles per day."
)

pdf.output("/Users/silversurfer/.gemini/antigravity-ide/brain/285de59e-9af1-43eb-b7e0-1c5df17d7374/sky_auto_calculator_guide.pdf")
print("PDF generated successfully.")
