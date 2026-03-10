import cv2
import numpy as np
import sys
from pathlib import Path

def extract_green_signature(image_path: str, output_path: str = None, debug: bool = True):
    """
    Extracts green ink signature from a timetable with overlapping printed black text.
    Uses LAB color space 'a' channel — the most reliable method for green ink isolation.

    Args:
        image_path  : Path to the input timetable image
        output_path : Where to save the extracted signature (optional)
        debug       : If True, saves intermediate steps for inspection

    Returns:
        signature_clean : The extracted signature as a binary mask (numpy array)
    """

    # ── 1. LOAD IMAGE ──────────────────────────────────────────────────────────
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")

    original = img.copy()
    print(f"[✓] Loaded image: {img.shape[1]}x{img.shape[0]} px")

    # ── 2. CONVERT TO LAB COLOR SPACE ─────────────────────────────────────────
    # LAB separates color from lightness. 'a' channel = green(-) vs red(+)
    # Black printed text → 'a' ≈ 128 (neutral)
    # Green ink signature → 'a' << 128 (strongly green = lower values)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    L, a, b = cv2.split(lab)

    print(f"[✓] LAB conversion done | 'a' channel min={a.min()}, max={a.max()}, mean={a.mean():.1f}")

    # ── 3. ISOLATE GREEN FROM 'a' CHANNEL ─────────────────────────────────────
    # In OpenCV, LAB 'a' is stored as 0–255 (128 = neutral)
    # Green pixels → values BELOW 128 (typically 90–120 range)
    # Black text   → values NEAR 128
    # White paper  → values NEAR 128

    # Invert: green becomes bright white, everything else dark
    a_inverted = 255 - a

    # Threshold: keep only distinctly green pixels
    # Adjust threshold (135–160) if your green is darker/lighter
    _, green_mask = cv2.threshold(a_inverted, 135, 255, cv2.THRESH_BINARY)

    # Alternative: use Otsu auto-thresholding (uncomment if above doesn't work)
    # _, green_mask = cv2.threshold(a_inverted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    print(f"[✓] Green mask: {np.count_nonzero(green_mask)} green pixels found")

    # ── 4. MORPHOLOGICAL CLEANUP ───────────────────────────────────────────────
    # Remove tiny noise dots (salt/pepper from scanning)
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    cleaned = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel_open, iterations=1)

    # Close small gaps within signature strokes
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel_close, iterations=2)

    # ── 5. REMOVE SMALL BLOBS (stray noise/dots) ──────────────────────────────
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(cleaned)
    min_blob_area = 50  # pixels — tune this if strokes are thin
    final_mask = np.zeros_like(cleaned)

    kept = 0
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_blob_area:
            final_mask[labels == i] = 255
            kept += 1

    print(f"[✓] Kept {kept} signature components after noise removal")

    # ── 6. CREATE CLEAN WHITE-BACKGROUND OUTPUT ────────────────────────────────
    # Signature strokes = black, background = white (standard for verification)
    signature_on_white = np.full_like(cv2.cvtColor(original, cv2.COLOR_BGR2GRAY), 255)
    signature_on_white[final_mask == 255] = 0

    # ── 7. CROP TO SIGNATURE BOUNDING BOX ─────────────────────────────────────
    coords = cv2.findNonZero(final_mask)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        padding = 20
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(img.shape[1], x + w + padding)
        y2 = min(img.shape[0], y + h + padding)
        cropped_signature = signature_on_white[y1:y2, x1:x2]
        print(f"[✓] Signature cropped to: {w}x{h} px (with {padding}px padding)")
    else:
        cropped_signature = signature_on_white
        print("[!] Warning: No signature pixels found — check your green threshold")

    # ── 8. SAVE OUTPUTS ────────────────────────────────────────────────────────
    base = Path(image_path).stem
    out_dir = Path(output_path).parent if output_path else Path(image_path).parent

    # Main output: clean cropped signature
    final_out = output_path or str(out_dir / f"{base}_signature_extracted.png")
    cv2.imwrite(final_out, cropped_signature)
    print(f"[✓] Saved extracted signature → {final_out}")

    if debug:
        # Save intermediate steps to understand what's happening
        cv2.imwrite(str(out_dir / f"{base}_debug_a_channel.png"), a)
        cv2.imwrite(str(out_dir / f"{base}_debug_a_inverted.png"), a_inverted)
        cv2.imwrite(str(out_dir / f"{base}_debug_green_mask_raw.png"), green_mask)
        cv2.imwrite(str(out_dir / f"{base}_debug_mask_final.png"), final_mask)
        print(f"[✓] Debug images saved to: {out_dir}")

    return cropped_signature, final_mask


# ── OVERLAY VISUALIZATION ──────────────────────────────────────────────────────
def visualize_overlay(image_path: str, mask: np.ndarray):
    """Shows original image with signature highlighted in red for verification."""
    img = cv2.imread(image_path)
    overlay = img.copy()
    overlay[mask == 255] = [0, 0, 255]  # highlight signature in red
    result = cv2.addWeighted(img, 0.5, overlay, 0.5, 0)
    out_path = str(Path(image_path).parent / (Path(image_path).stem + "_overlay.png"))
    cv2.imwrite(out_path, result)
    print(f"[✓] Overlay visualization saved → {out_path}")


# ── MAIN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clean_sign.py signatures\location\loc5.jpeg final_sign.png")
        # print("Example: python extract_signature.py timetable.jpg signature_out.png")
        sys.exit(1)

    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    signature, mask = extract_green_signature(image_path, output_path, debug=True)
    visualize_overlay(image_path, mask)

    print("\n── DONE ──────────────────────────────────────────────────────────────")
    print("Check the output files. If signature is incomplete or has noise:")
    print("  • Lower threshold (e.g. 130) → captures more green pixels")
    print("  • Raise threshold (e.g. 145) → removes more background noise")
    print("  • Reduce min_blob_area (e.g. 20) → keeps finer strokes")