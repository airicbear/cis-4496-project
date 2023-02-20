from .consts import BATCH_SIZE
from .diffaugment import data_augment_flip
from .create_model import cycle_gan_model, cycle_gan_compile_with_loss_rate
from .datasets import get_gan_dataset, get_gan_dataset_basic


if __name__ == '__main__':
    """
    Trains the configured model
    """

    BATCH_SIZE = 128
    # full_dataset = get_gan_dataset(augment=data_augment_flip,
    #                                shuffle=False,
    #                                batch_size=BATCH_SIZE)

    full_dataset = get_gan_dataset_basic()

    cycle_gan_compile_with_loss_rate(2e-4)
    cycle_gan_model.fit(full_dataset,
                        epochs=1,
                        steps_per_epoch=1)

    # cycle_gan_compile_with_loss_rate(1e-4)
    # cycle_gan_model.fit(full_dataset,
    #                     epochs=1,
    #                     steps_per_epoch=1)
    #
    # cycle_gan_compile_with_loss_rate(1e-5)
    # cycle_gan_model.fit(full_dataset,
    #                     epochs=1,
    #                     steps_per_epoch=1)

    cycle_gan_model.monet_generator.save_weights(f'photo2monet.h5')
    cycle_gan_model.photo_generator.save_weights(f'monet2photo.h5')
