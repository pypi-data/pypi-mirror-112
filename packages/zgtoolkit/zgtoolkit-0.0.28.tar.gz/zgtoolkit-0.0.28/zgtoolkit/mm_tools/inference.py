from mmdet.apis import init_detector, inference_detector
from zgtoolkit.dataset import parse_txt

# Specify the path to model config and checkpoint file
config_file = 'config.py'
checkpoint_file = 'workdir/latest.pth'

# build the model from a config file and a checkpoint file
model = init_detector(config_file, checkpoint_file, device='cuda:0')

results = parse_txt(r'anno/test.txt')

for res in results:
    image_path = res['image_path']
    result = inference_detector(model, image_path)
    # visualize the results in a new window
    model.show_result(image_path, result, show=True)
