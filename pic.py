import os
import math
from PIL import Image

def make_4_3_collage(src_folder, out_path,
                      target_width=1600,
                      padding=5,
                      exts=('.jpg', '.jpeg', '.png', '.bmp')):
    """
    生成一张 4:3 大图，自动遍历 src_folder 下所有图片（含子目录）并拼贴。
    
    参数:
      - src_folder: 源图片根目录
      - out_path: 保存拼贴图的路径
      - target_width: 最终拼贴图宽度，单位像素（高将自动按 4:3 计算）
      - padding: 每张小图之间的间距（像素）
      - exts: 支持的图片后缀
    """
    # 1. 递归收集所有图片路径
    paths = []
    for root, _, files in os.walk(src_folder):
        for fn in files:
            if fn.lower().endswith(exts):
                paths.append(os.path.join(root, fn))
    if not paths:
        raise RuntimeError(f"No images found in {src_folder}")

    n = len(paths)

    # 2. 根据目标宽高比(4:3)和图片数量，计算行列
    #    假设 cols/rows ~= 4/3 且 cols*rows >= n
    #    我们枚举可能的 row 数量，选择最接近平衡的
    best = None
    for rows in range(1, n+1):
        cols = math.ceil(n / rows)
        ratio = (cols/rows) / (4/3)
        # 记录最接近 1 的 ratio
        diff = abs(ratio - 1)
        if best is None or diff < best[0]:
            best = (diff, rows, cols)
    _, rows, cols = best

    total_slots = rows * cols
    # 3. 如果不够，用前序图片循环填充
    imgs = [Image.open(p).convert('RGB') for p in paths]
    for i in range(total_slots - n):
        imgs.append(imgs[i % n].copy())

    # 4. 计算每个格子的尺寸
    #    总宽 = target_width; 每列宽 = (target_width - padding*(cols-1))//cols
    cell_w = (target_width - padding*(cols-1)) // cols
    cell_h = int(cell_w * 3/4)  # 保持 4:3 格子比例

    # 5. 最终大图的高度
    target_height = rows * cell_h + padding*(rows-1)

    # 6. 创建画布
    canvas = Image.new('RGB', (target_width, target_height), (240,240,240))

    # 7. 缩放并粘贴
    idx = 0
    y = 0
    for r in range(rows):
        x = 0
        for c in range(cols):
            im = imgs[idx]
            im = im.resize((cell_w, cell_h), Image.LANCZOS)
            canvas.paste(im, (x, y))
            x += cell_w + padding
            idx += 1
        y += cell_h + padding

    # 8. 保存
    canvas.save(out_path)
    print(f"4:3 collage saved to {out_path}")

if __name__ == "__main__":
    make_4_3_collage(
        src_folder="fig/",
        out_path="fig/collage_4_3.jpg",
        target_width=1600,
        padding=5
    )
