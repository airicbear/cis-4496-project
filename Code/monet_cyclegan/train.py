from .consts import BATCH_SIZE
from .create_model import cycle_gan_model, cycle_gan_compile_with_loss_rate
from .datasets import load_dataset


if __name__ == '__main__':
    """
    Trains the configured model
    """

    full_dataset = load_dataset(BATCH_SIZE)

    cycle_gan_compile_with_loss_rate(2e-4)
    cycle_gan_model.fit(full_dataset, epochs=1,)

    cycle_gan_model.monet_generator.save_weights(f'photo2monet.h5')
    cycle_gan_model.photo_generator.save_weights(f'monet2photo.h5')
