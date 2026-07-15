from . import models

SEED_PRODUCTS = [
    {"name": "Meridian", "gender": "men", "price": 420, "dial": "#121212", "strap": "#1F1F1F", "accent": "#C1272D", "description": "A matte black case paired with a brushed steel bezel. Built for the boardroom and the runway alike, the Meridian carries a 41mm case and a 100m water resistance rating.", "popularity": 92},
    {"name": "Onyx Classic", "gender": "men", "price": 380, "dial": "#1a1a1a", "strap": "#8A8A8E", "accent": "#C1272D", "description": "Deep onyx dial with a sunburst finish, framed in a slim 38mm stainless case. A quiet, confident everyday watch.", "popularity": 76},
    {"name": "Ashcroft", "gender": "men", "price": 540, "dial": "#0d0d0d", "strap": "#121212", "accent": "#FAF9F6", "description": "Full-black tone-on-tone construction with a sapphire crystal and a titanium caseback. Our most technical men's piece.", "popularity": 88},
    {"name": "Nocturne", "gender": "men", "price": 460, "dial": "#171717", "strap": "#C1272D", "accent": "#121212", "description": "A black dial with a signature red second hand, set on a matte black leather strap. Named for its low-light legibility.", "popularity": 81},
    {"name": "Sable", "gender": "men", "price": 310, "dial": "#2a2a2a", "strap": "#8A8A8E", "accent": "#121212", "description": "Everyday minimalism: a clean three-hand movement, brushed steel strap, and a 40mm case that wears close to the wrist.", "popularity": 63},
    {"name": "Ferro", "gender": "men", "price": 610, "dial": "#101010", "strap": "#1F1F1F", "accent": "#C1272D", "description": "Our flagship chronograph. Two red sub-dials break up an otherwise all-black face built around an in-house movement.", "popularity": 95},
    {"name": "Vantage", "gender": "men", "price": 350, "dial": "#1c1c1c", "strap": "#8A8A8E", "accent": "#FAF9F6", "description": "A field-watch silhouette in matte black, with luminous markers and a canvas-textured strap.", "popularity": 58},
    {"name": "Ridgeline", "gender": "men", "price": 495, "dial": "#141414", "strap": "#121212", "accent": "#C1272D", "description": "Rugged and refined, the Ridgeline pairs a fluted bezel with a matte black finish strip across the dial.", "popularity": 70},
    {"name": "Lumen", "gender": "women", "price": 340, "dial": "#FAF9F6", "strap": "#8A8A8E", "accent": "#C1272D", "description": "An ivory dial in a slim 32mm case, finished with a delicate steel mesh strap. Understated and precise.", "popularity": 84},
    {"name": "Ivory Bloom", "gender": "women", "price": 300, "dial": "#F5F3EE", "strap": "#ECEAE5", "accent": "#121212", "description": "Soft ivory tones with a floral-etched caseback. A gentle, everyday companion piece.", "popularity": 66},
    {"name": "Aurelia", "gender": "women", "price": 460, "dial": "#121212", "strap": "#8A8A8E", "accent": "#C1272D", "description": "A black dial set in a rose-brushed case, with a fine link bracelet. Aurelia is built for evenings.", "popularity": 90},
    {"name": "Petra", "gender": "women", "price": 275, "dial": "#1a1a1a", "strap": "#1F1F1F", "accent": "#FAF9F6", "description": "A compact 30mm matte black case with a woven leather strap. Petra layers easily with everyday jewelry.", "popularity": 55},
    {"name": "Selene", "gender": "women", "price": 520, "dial": "#0d0d0d", "strap": "#C1272D", "accent": "#121212", "description": "Moonlit black dial, red leather strap. Selene is a limited seasonal release with a sapphire crystal front.", "popularity": 87},
    {"name": "Marlow", "gender": "women", "price": 315, "dial": "#F5F3EE", "strap": "#121212", "accent": "#C1272D", "description": "Ivory dial, matte black strap. A study in contrast, built on a slim quartz movement.", "popularity": 61},
    {"name": "Opaline", "gender": "women", "price": 395, "dial": "#EDEAE3", "strap": "#8A8A8E", "accent": "#121212", "description": "Opaline dial finish with a fine steel bracelet. A soft, quiet everyday luxury piece.", "popularity": 73},
    {"name": "Wren", "gender": "women", "price": 260, "dial": "#121212", "strap": "#8A8A8E", "accent": "#FAF9F6", "description": "Petite 28mm matte black case. Wren is our lightest, most minimal women's watch.", "popularity": 68},
]


def seed_products(db):
    """Populate the catalog on first run only — never overwrites existing data."""
    if db.query(models.Product).count() > 0:
        return
    for p in SEED_PRODUCTS:
        db.add(models.Product(**p, image_url=None))
    db.commit()
