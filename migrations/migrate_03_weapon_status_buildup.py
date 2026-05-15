import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'elden_lord.db')

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running migration: Add all innate status buildup columns to WEAPONS...")

    # All status buildup types in Elden Ring.
    # has_innate_bleed already exists from db_setup.py (v1).
    # All others added here as one logical schema decision.
    #
    # Scaling convention: standard affinity, max upgrade level.
    # Affinity-specific status scaling deferred to v3+.
    #
    # Notes per status type:
    #
    # MADNESS:
    #   Two distinct mechanics — damage and buildup are separate:
    #   - Proc damage: scales with the seal's Faith-based Incantation Scaling.
    #   - Buildup rate: scales with Arcane. Dragon Communion Seal boosts both.
    #   Mind governs resistance to madness, not damage output.
    #   IMPORTANT: Most non-NPC enemies are completely immune to madness.
    #   Buildup is far less viable in PvE than bleed or frost as a result.
    #   Primary use cases are PvP and specific NPC/humanoid enemies.
    #
    # FROST:
    #   Frostbite buildup is determined solely by weapon upgrade level.
    #   A +25 weapon has higher frost buildup than a +13 weapon.
    #   COMMON MISCONCEPTION: Cold affinity weapons scale with Intelligence,
    #   but that INT scaling only affects the weapon's damage output — NOT
    #   the frost buildup rate. Pumping INT does not increase how fast you
    #   proc frostbite. This is unlike bleed where Arcane directly increases
    #   buildup rate. No stat investment of any kind increases frost proc rate.
    #   Only weapon upgrade level matters for buildup.
    #   On proc: deals damage based on max HP and increases damage
    #   taken by 20% for 30 seconds - making it extremely valuable
    #   as a damage amplifier rather than a direct damage source.
    #
    # SLEEP:
    #   Genuine buildup that works on most enemies and some bosses.
    #   Notable PvE use case: Godskin Duo - sleep is a well-known cheese
    #   strategy for this fight. Many field enemies are also susceptible.
    #   Eternal Sleep (DLC variant) is stronger - targets won't wake when
    #   attacked, though bosses eventually wake after extended time.
    #   Resistance determined by Focus stat (scales with Mind).
    #
    # DEATH BLIGHT:
    #   Technically a buildup mechanic but extremely limited in practice.
    #   ONLY affects players, player-modeled NPCs, and Spirit Ashes.
    #   All other enemies and bosses are completely immune.
    #   Only one weapon in the game triggers it - via weapon skill, not
    #   innate passive hits. Essentially a PvP-only gimmick.
    #   Do not build around this expecting PvE viability.

    columns = [
        "has_innate_madness",
        "has_innate_frost",
        "has_innate_poison",
        "has_innate_scarlet_rot",
        "has_innate_sleep",
        "has_innate_death_blight",
    ]

    for col_name in columns:
        try:
            cursor.execute(f"""
                ALTER TABLE WEAPONS ADD COLUMN {col_name} BOOL DEFAULT 0
            """)
            print(f"  [OK] Added {col_name}")
        except Exception as e:
            print(f"  [SKIP] {col_name} may already exist: {e}")

    # Backfill note:
    # All v1 seed weapons have has_innate_bleed already set correctly.
    # No v1 weapons have any other innate status buildup - no backfill needed.

    # Verify schema
    cursor.execute("PRAGMA table_info(WEAPONS)")
    columns_info = cursor.fetchall()
    print("\n  Current WEAPONS columns:")
    for col in columns_info:
        print(f"    {col[1]} ({col[2]})")

    conn.commit()
    conn.close()
    print("\nMigration complete.")

if __name__ == "__main__":
    migrate()