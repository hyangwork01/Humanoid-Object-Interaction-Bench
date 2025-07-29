import os
from PIL import Image

def make_fixed_6x6_4_3_collage(src_folder, out_path,
                                target_width=1600,
                                padding=5,
                                exts=('.jpg', '.jpeg', '.png', '.bmp')):
    """
    在 src_folder 下递归收集所有图片（含子目录），
    固定 6 列 × 6 行布局，生成一张严格 4:3 比例的拼贴图并保存。
    """
    # 1. 收集所有图片路径
    paths = []
    for root, _, files in os.walk(src_folder):
        for fn in files:
            if fn.lower().endswith(exts):
                paths.append(os.path.join(root, fn))
    if not paths:
        raise RuntimeError(f"No images found in {src_folder}")

    # 2. 固定行列
    rows = cols = 6
    total_slots = rows * cols

    # 3. 加载并循环填充图片列表至 36 张
    imgs = [Image.open(p).convert('RGB') for p in paths]
    for i in range(total_slots - len(imgs)):
        imgs.append(imgs[i % len(imgs)].copy())

    # 4. 确定目标画布大小（4:3）
    target_height = int(target_width * 3 / 4)

    # 5. 计算每个网格 cell 的尺寸
    cell_w = (target_width  - padding * (cols - 1)) // cols
    cell_h = (target_height - padding * (rows - 1)) // rows

    # 6. 新建画布
    canvas = Image.new('RGB', (target_width, target_height), (240,240,240))

    # 7. 缩放并按行列粘贴
    idx = 0
    for r in range(rows):
        y = r * (cell_h + padding)
        for c in range(cols):
            x = c * (cell_w + padding)
            im = imgs[idx].resize((cell_w, cell_h), Image.LANCZOS)
            canvas.paste(im, (x, y))
            idx += 1

    # 8. 保存结果
    canvas.save(out_path)
    print(f"4:3 fixed 6×6 collage saved to {out_path}")

if __name__ == "__main__":
    make_fixed_6x6_4_3_collage(
        src_folder="fig/",
        out_path="fig/collage_4_3_6x6.jpg",
        target_width=1600,
        padding=5
    )
