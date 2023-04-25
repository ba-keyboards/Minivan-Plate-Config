import os
import shutil
import matplotlib.pyplot as plt
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import glob
import re
import os

class DXF2IMG(object):

    default_img_format = '.png'
    default_img_res = 300

    def convert_dxf2img(self, names, img_format=default_img_format, img_res=default_img_res):
        for name in names:
            # Check if a PNG file with the same name already exists in the 'all_preview' folder
            png_name = os.path.join('all_preview', os.path.splitext(os.path.basename(name))[0] + img_format)
            if os.path.isfile(png_name):
                print(f'{png_name} already exists, skipping conversion...')
                continue

            doc = ezdxf.readfile(name)
            msp = doc.modelspace()
            # Recommended: audit & repair DXF document before rendering
            auditor = doc.audit()
            # The auditor.errors attribute stores severe errors,
            # which *may* raise exceptions when rendering.
            if len(auditor.errors) != 0:
                raise Exception("The DXF document is damaged and can't be converted!")
            else:
                fig = plt.figure()
                ax = fig.add_axes([0, 0, 1, 1])
                ctx = RenderContext(doc)
                ctx.set_current_layout(msp)
                ctx.current_layout.set_colors(bg='#FFFFFF')
                out = MatplotlibBackend(ax)
                Frontend(ctx, out).draw_layout(msp, finalize=True)

                img_name = re.findall("(\S+)\.", name)  # select the image name that is the same as the dxf file name
                first_param = ''.join(img_name) + img_format  # concatenate list and string
                out_path = os.path.join('all_preview', first_param)
                fig.savefig(out_path, dpi=img_res)
                plt.close()

if __name__ == '__main__':
    dxf_files = glob.glob('all_dxf/*.DXF')
    converter = DXF2IMG()
    converter.convert_dxf2img(dxf_files, img_format='.png')
