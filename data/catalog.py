"""Product content for supplementsbyhazel.com.

Each product page is built from one entry here (see build.py). Prices, stock and subscription
plans are NOT here: they're read live from Wix Stores on the page, by the slugs in `packs`.
Each pack size is its own Wix product (1, 3 and 6 tubs), each with its own Subscribe & save plan.

Health claims are the authorised EU/UK register wording used on the current site; claims marked
with * on the page are covered by the footnote. Edit text freely, but keep claims to that register.
"""

W = "https://static.wixstatic.com/media/"

# One-line shared notices
FOOD_SUPPLEMENT = ("Food supplements should not be used as a substitute for a varied, balanced diet "
                   "and a healthy lifestyle. Do not exceed the recommended daily dose. Keep out of reach "
                   "of children. If you are pregnant, breastfeeding, taking medication or have a medical "
                   "condition, speak to a healthcare professional before use.")
CLAIMS_NOTE = "*Claims authorised under the EU/UK Nutrition and Health Claims Register."

PRODUCTS = {
    "clarity": {
        "benefits": ["Reduction of tiredness and fatigue*", "Normal psychological function*", "Maintenance of normal bones*"],
        "badges": ["Vegan"],
        "goals": ["energy", "mood", "bones", "immunity", "menopause", "perimenopause"],
        "file": "clarity.html",
        "name": "Clarity",
        "acc": "clarity",
        "stage": "Midlife",
        "menu_note": "Daily support through midlife",
        "card": "Magnesium, vitamin D, B12 and live cultures in one daily capsule.",
        "tagline": "Daily nutritional support for midlife wellbeing",
        "title": "Clarity | Midlife Supplement with Magnesium, Vitamin D & B12",
        "description": "Clarity is a once-a-day midlife supplement with magnesium, vitamin D, vitamin B12 and live cultures. Vegan. Formulated by Hazel Hayden, made in the UK.",
        "image": W + "f6f1f2_f1f3c1354585418fb9929cf94dbaf4fa~mv2.png",
        "gallery": [W + "f6f1f2_f1f3c1354585418fb9929cf94dbaf4fa~mv2.png", W + "f6f1f2_f199536e87c94870b0270cf6d309aa1d~mv2.png"],
        "alt": "A tub of Clarity by Supplements by Hazel, with a yellow label",
        "packs": [("clarity", "1 tub", "1 month"), ("clarity-3-tubs-save-10", "3 tubs", "Save 10%"), ("clarity-6-tubs-save-15", "6 tubs", "Save 15%")],
        "chips": ["One capsule a day", "Vegan", "Made in the UK"],
        "intro": [
            "Clarity is one capsule a day with four ingredients: magnesium, vitamin D, vitamin B12 and live cultures. Hazel chose them for the years around the menopause.",
            "Take it alongside a varied, balanced diet.",
        ],
        "why": [
            ("Four ingredients", "Magnesium, vitamin D and vitamin B12 for energy, bones and psychological function.*"),
            ("One capsule a day", "Take it with breakfast or lunch."),
            ("Vegan", "No animal-derived ingredients, gelatine, artificial colours or flavours."),
            ("Made by a menopause specialist", "Formulated by Hazel Hayden, who has 38 years of clinical experience in the NHS."),
        ],
        "note": "Clarity was created to simplify daily nutrition without compromising on quality. Each ingredient has been carefully chosen to support everyday wellbeing.",
        "formula_intro": "What each ingredient does, in the wording the UK and EU allow.*",
        "ingredients": [
            ("Magnesium", "For energy, bones and mind", ["Contributes to the maintenance of normal bones*", "Contributes to normal psychological function*", "Contributes to normal energy-yielding metabolism and the reduction of tiredness and fatigue*", "Contributes to normal muscle function*"]),
            ("Vitamin D", "For bones, muscles and immunity", ["Contributes to the maintenance of normal bones and muscle function*", "Contributes to the normal function of the immune system*", "Contributes to the normal absorption and utilisation of calcium and phosphorus*"]),
            ("Vitamin B12", "For energy and the nervous system", ["Contributes to normal energy-yielding metabolism*", "Contributes to the normal function of the nervous system*", "Contributes to normal psychological function*", "Contributes to the reduction of tiredness and fatigue*"]),
            ("Live cultures", "Lactobacillus and Bifidobacterium", ["Strains that occur naturally in the human gut"]),
        ],
        "how": "Take one capsule a day with a meal and a glass of water. Many people take it with breakfast or lunch.",
        "review": ("I've been taking this supplement for a couple of months and didn't realise how good it made me feel until I ran out. I won't be doing that again! I feel more balanced with more energy.", "Janey, April 2024"),
        "faqs": [
            ("Is Clarity suitable for vegetarians and vegans?", ["Yes. Clarity is suitable for both vegetarians and vegans. The capsule and all the ingredients are free from animal-derived products, and we don't use gelatine or other animal-based binders.", "If you follow a plant-based diet, Clarity can help you get nutrients that can be harder to obtain from food alone, such as vitamin B12 and vitamin D."]),
            ("How should I take Clarity?", ["Take one capsule a day, ideally with a meal and a glass of water. Taking it with food helps the absorption of some nutrients and makes it part of your routine.", "Do not exceed the recommended daily dose. Clarity can be taken all year round."]),
            ("Are there any side effects?", ["Clarity's ingredients are generally well tolerated. As with any food supplement, individual responses vary: some people notice mild digestive changes, particularly if they're new to live cultures.", "If you notice any unexpected effects, stop taking it and speak to a healthcare professional. Always read the ingredients if you have allergies or intolerances."]),
            ("Can I take Clarity with other supplements?", ["Clarity can be taken alongside many other supplements, but check the nutrient content of everything you take so you don't exceed recommended levels, for example if you already take a multivitamin.", "If you take prescription medication or have a medical condition, speak to your doctor or pharmacist first."]),
        ],
        "blog": "the-clarity-formula-a-daily-wellbeing-supplement-designed-to-support-modern-life",
        "related": ["peri", "rosy", "hair-skin"],
    },
    "peri": {
        "benefits": ["Maintenance of normal skin and hair*", "Normal energy-yielding metabolism*", "Ashwagandha and saffron"],
        "badges": ["Vegetarian"],
        "goals": ["perimenopause", "hair-skin", "energy"],
        "file": "peri.html",
        "name": "Peri",
        "acc": "peri",
        "stage": "Pre-midlife",
        "menu_note": "Botanicals and biotin for pre-midlife",
        "card": "Ashwagandha, saffron and biotin to support hair, skin and energy.",
        "tagline": "Daily nutritional support for pre-midlife",
        "title": "Peri | Perimenopause Supplement with Ashwagandha, Saffron & Biotin",
        "description": "Peri combines ashwagandha, saffron and biotin with essential vitamins and minerals to support hair, skin and energy in pre-midlife. Formulated by Hazel Hayden, made in the UK.",
        "image": W + "f6f1f2_9a962cb5e1664240a5851c60202ad7ec~mv2.png",
        "gallery": [W + "f6f1f2_9a962cb5e1664240a5851c60202ad7ec~mv2.png", W + "f6f1f2_c4ce7724e055492e9f70fdc718d44ae1~mv2.jpg", W + "f6f1f2_e3d2262ccdc440aea4d89b887e5b8b75~mv2.png"],
        "alt": "A tub of Peri by Supplements by Hazel, with a sky-blue label",
        "packs": [("peri", "1 tub", "1 month"), ("peri-3-tubs-save-10", "3 tubs", "Save 10%"), ("peri-6-tubs-save-15", "6 tubs", "Save 15%")],
        "chips": ["Ashwagandha and saffron", "Vegetarian", "Made in the UK"],
        "intro": [
            "Peri combines ashwagandha and saffron with biotin and other vitamins and minerals. Biotin helps maintain normal skin and hair, and supports normal energy-yielding metabolism.*",
            "Hazel made it for the years before the menopause, when periods start to change. Take it alongside a varied, balanced diet.",
        ],
        "why": [
            ("Made for the years before the menopause", "Biotin for normal skin, hair and energy-yielding metabolism.*"),
            ("Two botanicals", "Ashwagandha and saffron extract."),
            ("Taken with meals", "One capsule twice a day."),
            ("Made by a menopause specialist", "Formulated by Hazel Hayden, a Consultant Nurse who specialises in women's health."),
        ],
        "note": "Peri was created for those who want simplicity with quality: a thoughtfully crafted formula that fits into modern living.",
        "formula_intro": "Two botanicals and the vitamins and minerals that go with them.",
        "ingredients": [
            ("Ashwagandha and saffron", "Botanical extracts", ["Two plants with a long history of traditional use"]),
            ("Biotin (vitamin B7)", "For hair, skin and energy", ["Contributes to the maintenance of normal skin and hair*", "Contributes to normal energy-yielding metabolism*", "Contributes to the normal function of the nervous system*"]),
            ("Vitamins and minerals", "To go alongside your diet", ["A selection of vitamins and minerals; the full list is on the label"]),
        ],
        "how": "Take one capsule twice a day with water, preferably with meals.",
        "review": ("They are really helpful. I definitely notice the days that I don't take them. Highly recommend.", "Sarah, February 2024"),
        "faqs": [
            ("Is Peri suitable for vegetarians or vegans?", ["Peri is suitable for vegetarians, as it contains no meat, poultry or fish-derived ingredients. It is not suitable for vegans, because some vitamins or botanical carriers may be from non-vegan sources.", "Check the full ingredients list on the label to make sure it suits your diet."]),
            ("How do I take Peri?", ["Take one capsule twice a day with water, preferably with meals, to help absorption. Do not exceed the recommended daily dose."]),
            ("Who can take Peri?", ["Peri is designed for adult women in the pre-midlife phase, as part of a healthy, balanced lifestyle. It is not intended for children.", "If you are pregnant, breastfeeding, taking prescription medication or have a medical condition, speak to a healthcare professional first."]),
            ("Are there any side effects?", ["Peri's ingredients are generally well tolerated, but individual responses vary. If you notice any unwanted effects, such as digestive discomfort or an allergic reaction, stop taking it and speak to a healthcare professional."]),
        ],
        "blog": "the-peri-formula-botanical-nutritional-support-for-perimenopause-and-midlife-wellbeing",
        "related": ["clarity", "hair-skin", "wellbeing"],
    },
    "rosy": {
        "benefits": ["Normal psychological function*", "Normal collagen formation*", "Maintenance of normal bones*"],
        "badges": ["Vegan"],
        "goals": ["post", "mood", "bones", "immunity"],
        "file": "rosy.html",
        "name": "Rosy",
        "acc": "rosy",
        "stage": "Post-midlife",
        "menu_note": "An evening capsule for post-midlife",
        "card": "Vitamins C and D3, L-theanine, astaxanthin and lycopene, taken in the evening.",
        "tagline": "Supporting you through post-midlife",
        "title": "Rosy | Post-Midlife Supplement with Vitamin C, D3 & L-Theanine",
        "description": "Rosy is an evening supplement with vitamin C, vitamin D3, L-theanine, astaxanthin, citrus bioflavonoids and lycopene. Vegan. Formulated by Hazel Hayden, made in the UK.",
        "image": W + "f6f1f2_824eec1739de42f1a28f06196429ed1e~mv2.jpg",
        "gallery": [W + "f6f1f2_824eec1739de42f1a28f06196429ed1e~mv2.jpg", W + "f6f1f2_48f3f80fdb3e4acca2cf4dcaf1812ef9~mv2.png", W + "f6f1f2_cfe3a11c76fb48bab09b78f89c81b3e1~mv2.png"],
        "alt": "A tub of Rosy by Supplements by Hazel, with a lavender label",
        "packs": [("rosy", "1 tub", "1 month"), ("rosy-3-tubs-save-10", "3 tubs", "Save 10%"), ("rosy-6-tubs-save-15", "6 tubs", "Save 15%")],
        "chips": ["One capsule in the evening", "Vegan", "Made in the UK"],
        "intro": [
            "Rosy is one capsule taken in the evening. It has vitamin C and vitamin D3, plus four plant compounds: L-theanine, astaxanthin, citrus bioflavonoids and lycopene.",
            "Hazel made it for the years after the menopause. Take it alongside a varied, balanced diet.",
        ],
        "why": [
            ("Made by a menopause specialist", "Formulated by Hazel Hayden, who has 38 years of clinical experience in the NHS."),
            ("Vitamins C and D3", "For collagen formation, psychological function, bones and immunity.*"),
            ("One evening capsule", "Taken before bed, as part of your evening routine."),
            ("Vegan", "Free from animal-derived products, gelatine, artificial colours and flavours."),
        ],
        "note": "Rosy is about refinement in nutrition: a daily ritual to complement life's many possibilities.",
        "formula_intro": "Two vitamins and four plant compounds in one capsule.",
        "ingredients": [
            ("Vitamin C", "For collagen, energy and mind", ["Contributes to normal collagen formation*", "Contributes to normal psychological function*", "Contributes to the protection of cells from oxidative stress*", "Contributes to normal energy-yielding metabolism*"]),
            ("Vitamin D3", "For bones, muscles and immunity", ["Contributes to the maintenance of normal bones and teeth*", "Contributes to the maintenance of normal muscle function*", "Contributes to the normal function of the immune system*", "Contributes to the normal absorption and utilisation of calcium and phosphorus*"]),
            ("L-theanine and citrus bioflavonoids", "Plant compounds", ["Plant compounds from tea and citrus fruit"]),
            ("Astaxanthin and lycopene", "Carotenoids", ["The pigments that colour algae and tomatoes red"]),
        ],
        "how": "Take one capsule in the evening before bed, with water.",
        "review": ("I'm back in the land of the living! Absolute game changer. Have been recommending it to all my friends.", "Sarah, January 2024"),
        "faqs": [
            ("How should I take Rosy?", ["Take one capsule in the evening before bed, swallowed with water. Do not exceed the recommended daily dose."]),
            ("Is Rosy suitable for vegetarians or vegans?", ["Yes. Rosy is suitable for both vegetarians and vegans. The capsule and all the ingredients are free from animal-derived products, and we avoid gelatine, artificial colours and flavours."]),
            ("Can I take Rosy with other medication or supplements?", ["If you take prescription medication, are pregnant or breastfeeding, or have a medical condition, speak to a healthcare professional before starting Rosy or any new supplement."]),
            ("Are there any side effects?", ["Rosy is generally well tolerated, but some people may be sensitive to certain ingredients. If you notice any adverse effects, stop taking it and speak to a healthcare professional."]),
        ],
        "blog": "rosy-premium-daily-nutrition-for-beauty-wellbeing-and-modern-living",
        "related": ["clarity", "hair-skin", "hormone"],
    },
    "hair-skin": {
        "benefits": ["Maintenance of normal skin, hair and nails*", "Normal collagen formation*", "With marine collagen"],
        "badges": [],
        "goals": ["hair-skin", "immunity", "menopause"],
        "file": "hair-skin.html",
        "name": "Hair & Skin",
        "acc": "hair-skin",
        "stage": "Every stage",
        "menu_note": "Vitamin C, biotin, zinc and marine collagen",
        "card": "Vitamin C, biotin, zinc and marine collagen for hair, skin and nails.",
        "tagline": "Daily nutritional support for healthy hair, skin and nails",
        "title": "Hair & Skin | Supplement with Marine Collagen, Biotin & Zinc",
        "description": "Hair & Skin combines vitamin C, biotin, zinc, marine collagen and botanicals to help maintain normal hair, skin and nails. Formulated by Hazel Hayden, made in the UK.",
        "image": W + "f6f1f2_25e8cfb57606462d8ddad7dae232f099~mv2.png",
        "gallery": [W + "f6f1f2_25e8cfb57606462d8ddad7dae232f099~mv2.png", W + "f6f1f2_323e9a7f2b69470fafd97b5762da6e6d~mv2.png", W + "f6f1f2_79f5d41dae3e494d87231ec3465ebe45~mv2.png"],
        "alt": "A tub of Hair & Skin by Supplements by Hazel, with a teal label",
        "packs": [("hair-skin", "1 tub", "1 month"), ("hair-skin-3-tubs-save-10", "3 tubs", "Save 10%"), ("hair-skin-6-tubs-save-15", "6 tubs", "Save 15%")],
        "chips": ["Marine collagen", "Biotin and zinc", "Made in the UK"],
        "intro": [
            "Hair & Skin has vitamin C, biotin, zinc, marine collagen and a blend of botanicals. Biotin and zinc help maintain normal hair and skin, and zinc normal nails.*",
            "Take it alongside a varied, balanced diet. It contains marine collagen, so it isn't suitable for vegetarians or vegans.",
        ],
        "why": [
            ("For hair, skin and nails", "Biotin and zinc help maintain normal hair, skin and nails.*"),
            ("Marine collagen", "Sustainably sourced, alongside a blend of botanicals."),
            ("Once a day", "Two capsules with a meal."),
            ("Made by a menopause specialist", "Formulated by Hazel Hayden, a Consultant Nurse who specialises in women's health."),
        ],
        "note": "Hair & Skin was created for those who appreciate premium nutrition with a beauty focus: simple, elegant and trustworthy.",
        "formula_intro": "What each ingredient does, in the wording the UK and EU allow.",
        "ingredients": [
            ("Vitamin C", "For collagen and skin", ["Contributes to normal collagen formation for the normal function of skin*", "Contributes to the protection of cells from oxidative stress*", "Contributes to the normal function of the immune system*", "Contributes to normal energy-yielding metabolism*"]),
            ("Biotin and zinc", "For hair, skin and nails", ["Biotin contributes to the maintenance of normal skin and hair*", "Zinc contributes to the maintenance of normal skin, hair and nails*", "Zinc contributes to normal macronutrient metabolism*"]),
            ("Marine collagen", "Protein from fish", ["Sustainably sourced. Not suitable for vegetarians or vegans"]),
            ("Botanicals", "A plant blend", ["The full list is on the label"]),
        ],
        "how": "Take two capsules once a day with water, ideally with a meal.",
        "review": ("I've noticed a remarkable difference since I started using these vitamins. I highly recommend them. It can be overwhelming trying to find the right advice in women's health, but Hazel is truly the perfect person to guide you.", "Gemma, September 2024"),
        "faqs": [
            ("How do I take Hair & Skin?", ["Take two capsules once a day with water, ideally with a meal to help absorption. Do not exceed the recommended daily intake."]),
            ("Is Hair & Skin suitable for vegetarians or vegans?", ["No. Hair & Skin contains marine collagen, so it isn't suitable for vegetarians or vegans.", "All Supplements by Hazel products are free from artificial additives, gluten, soy and dairy."]),
            ("Can I take it with other supplements or medication?", ["If you take prescription medication, are pregnant or breastfeeding, or have a medical condition, speak to a healthcare professional first. They can check for nutrient duplications or interactions."]),
            ("Are there any side effects?", ["Hair & Skin is generally well tolerated when taken as directed. Some people may be sensitive to certain vitamins, minerals or other ingredients. If you notice any unusual symptoms, stop taking it and seek advice from a healthcare professional."]),
        ],
        "blog": "hair-skin-daily-beauty-support-for-healthy-hair-skin-and-nails",
        "related": ["clarity", "rosy", "peri"],
    },
    "wellbeing": {
        "benefits": ["Clarity, Peri and Hair & Skin", "Save 10% on 3 months, 15% on 6", "Free gift with your first order"],
        "badges": ["Bundle & Save"],
        "goals": ["perimenopause", "energy", "hair-skin"],
        "file": "wellbeing-bundle.html",
        "name": "Wellbeing Support Bundle",
        "short": "Wellbeing Bundle",
        "acc": "wellbeing",
        "stage": "Bundle · pre-midlife",
        "menu_note": "Clarity, Peri and Hair & Skin",
        "card": "Clarity, Peri and Hair & Skin together, for the pre-midlife years.",
        "tagline": "Three formulas for the pre-midlife transition",
        "title": "Wellbeing Support Bundle | Clarity, Peri & Hair & Skin",
        "description": "Clarity, Peri and Hair & Skin together, for the years before the menopause. Save 10% on 3 months and 15% on 6. Free UK delivery.",
        "image": W + "f6f1f2_bb83496e97be48ff9efa0bc39f0fa360~mv2.png",
        "gallery": [W + "f6f1f2_bb83496e97be48ff9efa0bc39f0fa360~mv2.png", W + "f6f1f2_791e9ad1018c4c72bba515f69e074efe~mv2.jpg"],
        "alt": "Tubs of Peri, Clarity and Hair & Skin together on a sky-blue background",
        "packs": [("perimenopause-support", "1 month", "3 tubs"), ("wellbeing-support-3-months-supply-save-10", "3 months", "Save 10%"), ("wellbeing-support-6-months-supply-save-15", "6 months", "Save 15%")],
        "chips": ["Clarity + Peri + Hair & Skin", "Free gift on first order", "Made in the UK"],
        "intro": [
            "Clarity, Peri and Hair & Skin together, for the years before the menopause.",
            "Your first bundle order comes with a free supplement from the range.",
        ],
        "includes": ["clarity", "peri", "hair-skin"],
        "includes_notes": {"clarity": "Supports energy, bones and psychological function*", "peri": "Botanicals and biotin for hair, skin and energy*", "hair-skin": "Nutrients to help maintain normal skin, hair and nails*"},
        "review": ("I've been taking this supplement for a couple of months and didn't realise how good it made me feel until I ran out. I won't be doing that again! I feel more balanced with more energy.", "Janey, April 2024"),
        "related": ["hormone", "clarity", "peri"],
    },
    "hormone": {
        "benefits": ["Clarity, Rosy and Hair & Skin", "Save 10% on 3 months, 15% on 6", "Free gift with your first order"],
        "badges": ["Bundle & Save"],
        "goals": ["menopause", "post", "mood", "energy", "hair-skin"],
        "file": "hormone-health-bundle.html",
        "name": "Hormone Health Support Bundle",
        "short": "Hormone Health Bundle",
        "acc": "hormone",
        "stage": "Bundle · midlife",
        "menu_note": "Clarity, Rosy and Hair & Skin",
        "card": "Clarity, Rosy and Hair & Skin together, for wellbeing through midlife.",
        "tagline": "Three formulas for wellbeing through midlife",
        "title": "Hormone Health Support Bundle | Clarity, Rosy & Hair & Skin",
        "description": "Clarity, Rosy and Hair & Skin together, for the menopause and after. Save 10% on 3 months and 15% on 6. Free UK delivery.",
        "image": W + "f6f1f2_b18172219e194152b95ec0dc1a4557c6~mv2.png",
        "gallery": [W + "f6f1f2_b18172219e194152b95ec0dc1a4557c6~mv2.png", W + "f6f1f2_3cb788e1a5374015a537544155e5020d~mv2.png", W + "f6f1f2_f34381d9fe3f42409d5eff6c5dae06e6~mv2.png", W + "f6f1f2_48f3f80fdb3e4acca2cf4dcaf1812ef9~mv2.png"],
        "alt": "Tubs of Rosy, Clarity and Hair & Skin together on a teal background",
        "packs": [("hormone-health-support", "1 month", "3 tubs"), ("hormone-health-3-months-supply-save-10", "3 months", "Save 10%"), ("hormone-health-6-months-supply-save-15", "6 months", "Save 15%")],
        "chips": ["Clarity + Rosy + Hair & Skin", "Free gift on first order", "Made in the UK"],
        "intro": [
            "Clarity, Rosy and Hair & Skin together, for the menopause and the years after it.",
            "Your first bundle order comes with a free supplement from the range.",
        ],
        "includes": ["rosy", "clarity", "hair-skin"],
        "includes_notes": {"rosy": "Vitamins C and D3 with plant compounds, taken in the evening*", "clarity": "Helps reduce tiredness and fatigue*", "hair-skin": "Nutrients to help maintain normal skin, hair and nails*"},
        "review": ("These supplements are full of the nutrients you need and not fillers. Genuine product. Will buy again.", "Supplements by Hazel customer"),
        "related": ["wellbeing", "rosy", "clarity"],
    },
    "iron": {
        "benefits": ["50mg of elemental iron", "Vegetable cellulose capsule", "Two months' supply"],
        "badges": [],
        "goals": [],
        "file": "iron.html",
        "name": "High Strength Iron",
        "acc": "iron",
        "stage": "Essentials",
        "menu_note": "50mg iron, two months' supply",
        "card": "50mg of elemental iron in a vegetable cellulose capsule. Two months' supply.",
        "tagline": "A high-strength iron supplement",
        "title": "High Strength Iron Supplement | Supplements by Hazel",
        "description": "A high-strength iron supplement providing 50mg of elemental iron in a vegetable cellulose capsule. Two months' supply. From Supplements by Hazel.",
        "image": W + "f6f1f2_ab5b0898054d449d995ad253ff6612a7~mv2.webp",
        "gallery": [W + "f6f1f2_ab5b0898054d449d995ad253ff6612a7~mv2.webp"],
        "alt": "A tub of High Strength Iron Supplement",
        "packs": [("high-strength-iron-supplement", "1 tub", "2 months")],
        "chips": ["50mg elemental iron", "Vegetable capsule", "2 months' supply"],
        "intro": [
            "50mg of elemental iron in a vegetable cellulose capsule. Each tub lasts two months.",
        ],
        "how": "Take as directed on the label. Do not exceed the stated dose.",
        "faqs": [
            ("Who is it for?", ["Iron needs vary. If you think you may be low in iron, or you're unsure whether you need it, speak to your GP or pharmacist before taking an iron supplement."]),
            ("Can I take it with other supplements?", ["Check the iron content of everything you take, including multivitamins, so you don't exceed recommended levels. Keep iron supplements out of reach of children."]),
        ],
        "related": ["clarity", "rosy", "hair-skin"],
        "simple": True,
    },
}

# Shop by health goal: (key, label, short description). Products list their goals above.
GOALS = [
    ("energy", "Energy", "Tiredness and fatigue"),
    ("mood", "Mood & mind", "Psychological function"),
    ("hair-skin", "Hair, skin & nails", "Biotin, zinc and vitamin C"),
    ("bones", "Bones & muscles", "Vitamin D and magnesium"),
    ("immunity", "Immunity", "Vitamins C and D"),
    ("perimenopause", "Perimenopause", "When periods start to change"),
    ("menopause", "Menopause", "During the change"),
    ("post", "Post-menopause", "A year or more after your last period"),
]

# Order on the shop page and in the menu
SINGLES = ["clarity", "peri", "rosy", "hair-skin"]
BUNDLES = ["wellbeing", "hormone"]
EXTRAS = ["iron"]

TEAM = [
    ("Founder", "Hazel Hayden", "Consultant Nurse and British Menopause Society Registered Specialist, with 38 years in the NHS. Hazel formulates every product and decides what goes in it."),
    ("CEO", "Tim Hayden", "Tim has a background in business management and runs the company day to day."),
    ("Director of Operations", "Kim Jones", "Kim looks after stock, deliveries, suppliers and quality checks."),
    ("Social Media & Marketing", "Tia Brown", "Tia runs our social media and marketing, and answers many of your messages online."),
    ("Customer Service", "Amy Bold", "Amy answers most of our emails and calls, and can help with anything about your order."),
    ("Customer Service", "Neave Kerslake", "Neave joined from recruitment and office administration, and helps customers by phone and email."),
]

# Blog posts, newest first: (slug, title, date, image, minutes, excerpt). The page lists them live
# from Wix Blog; this copy is the no-JavaScript fallback and feeds the sitemap.
POSTS_FILE = "posts.json"
