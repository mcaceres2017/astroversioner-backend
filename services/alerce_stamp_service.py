from alerce.core import Alerce
import numpy as np
import matplotlib.pyplot as plt
import os
import io


# ojo con el cliente, si no me equivoco con el min estoy
# sacando la primera stamp en el historico de cada oid.
# tl;dr, la stamp mas vieja.


class AlerceStampService:
    client = Alerce()

    @staticmethod
    def get_stamps(detections):
        candids_df = detections.loc[detections.has_stamp]
        min_candids_series = candids_df.groupby("oid")["candid"].min()

        candid_oid = min_candids_series.index.tolist()
        min_candids = min_candids_series.values.tolist()

        stamps = []
        for i, c in enumerate(min_candids):
            candid_stamps = AlerceStampService.client.get_stamps(
                candid_oid[i], candid=c
            )
            stamps.append(candid_stamps)

        return stamps, candid_oid, min_candids

    @staticmethod
    def plot_and_save_stamps(stamps, candid_oid, min_candids):
        stamp_titles = ["science", "reference", "difference"]

        image_data_list = []  # to store the generated images as binary
        stamp_names = []  # in the order sci, ref, diff.

        for i, s in enumerate(stamps):
            science, ref, difference = s[0].data, s[1].data, s[2].data

            for idx, im in enumerate(
                [np.arcsinh(science), np.arcsinh(ref), difference]
            ):
                fig, ax = plt.subplots()
                ax.imshow(im, cmap="viridis")  # Log scale for visualization
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
                fig.subplots_adjust(wspace=0, hspace=0)

                stamp_name = (
                    str(candid_oid[i])
                    + "-"
                    + str(min_candids[i])
                    + "-"
                    + stamp_titles[idx]
                    + ".png"
                )

                buffer = io.BytesIO()  # Use io.BytesIO to store the binary data

                plt.savefig(
                    buffer,
                    format="png",
                    bbox_inches="tight",
                    pad_inches=0,
                )

                buffer.seek(0)  # Move the cursor to the beginning of the buffer

                # ojo aqui, estoy aprovechando el orden de las stamps, si no funciona,
                # crea una lista de tripletas.
                image_data_list.append(buffer.read())
                stamp_names.append(stamp_name)

                plt.close()

        return image_data_list, stamp_names

    @staticmethod
    def get_stamps_as_images(detections):
        stamps, candid_oid, min_candids = AlerceStampService.get_stamps(detections)
        return AlerceStampService.plot_and_save_stamps(stamps, candid_oid, min_candids)
