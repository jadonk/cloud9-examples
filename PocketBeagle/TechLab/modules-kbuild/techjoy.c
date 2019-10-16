/*
 * See https://github.com/konsulko/techjoy/blob/master/techjoy.c
 *
 * Techlab cape joystick input driver
 *
 * Copyright 2019 Konsulko Group
 * Matt Porter <mporter@konsulko.com>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation version 2.
 *
 * This program is distributed "as is" WITHOUT ANY WARRANTY of any
 * kind, whether express or implied; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 */

#include <linux/gpio/consumer.h>
#include <linux/iio/consumer.h>
#include <linux/iio/types.h>
#include <linux/input.h>
#include <linux/input-polldev.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/of.h>
#include <linux/platform_device.h>

struct techjoy {
	struct input_polled_dev *poll_dev;
	char phys[32];
	struct gpio_desc *btn_a, *btn_b;
	struct iio_channel *accel_x, *accel_y;
};

static void techjoy_poll(struct input_polled_dev *dev)
{
	struct techjoy *p = dev->private;
	int ret, a, b, x, y;

	a = gpiod_get_value(p->btn_a);
	input_report_key(dev->input, BTN_A, a);

	b = gpiod_get_value(p->btn_b);
	input_report_key(dev->input, BTN_B, b);

	ret = iio_read_channel_raw(p->accel_x, &x);
	if (unlikely(ret < 0))
		return;
	input_report_abs(dev->input, ABS_X, x);

	ret = iio_read_channel_raw(p->accel_y, &y);
	if (unlikely(ret < 0))
		return;
	input_report_abs(dev->input, ABS_Y, y);

	input_sync(dev->input);
}

static int techjoy_probe(struct platform_device *pdev)
{
	struct device *dev = &pdev->dev;
	struct techjoy *p;
	struct input_polled_dev *poll_dev;
	struct input_dev *input;
	enum iio_chan_type type;
	int ret;

	p = devm_kzalloc(dev, sizeof(*p), GFP_KERNEL);
	if (!p)
		return -ENOMEM;

	p->btn_a = devm_gpiod_get_index(dev, "button", 0, GPIOD_IN);
	if (IS_ERR(p->btn_a)) {
		ret = PTR_ERR(p->btn_a);
		dev_err(dev, "failed to get btn_a GPIO: %d\n", ret);
		return ret;
	}

	p->btn_b = devm_gpiod_get_index(dev, "button", 1, GPIOD_IN);
	if (IS_ERR(p->btn_b)) {
		ret = PTR_ERR(p->btn_b);
		dev_err(dev, "failed to get btn_b GPIO: %d\n", ret);
		return ret;
	}

	p->accel_x = devm_iio_channel_get(dev, "accel_x");
	if (IS_ERR(p->accel_x))
		return PTR_ERR(p->accel_x);

	if (!p->accel_x->indio_dev)
		return -ENXIO;

	ret = iio_get_channel_type(p->accel_x, &type);
	if (ret < 0)
		return ret;

	if (type != IIO_ACCEL) {
		dev_err(dev, "not accelerometer channel %d\n", type);
		return -EINVAL;
	}

	p->accel_y = devm_iio_channel_get(dev, "accel_y");
	if (IS_ERR(p->accel_y))
		return PTR_ERR(p->accel_y);

	if (!p->accel_y->indio_dev)
		return -ENXIO;

	ret = iio_get_channel_type(p->accel_y, &type);
	if (ret < 0)
		return ret;

	if (type != IIO_ACCEL) {
		dev_err(dev, "not accel channel %d\n", type);
		return -EINVAL;
	}

	poll_dev = devm_input_allocate_polled_device(dev);
	if (!poll_dev) {
		dev_err(dev, "unable to allocate input device\n");
		return -ENOMEM;
	}

	poll_dev->poll_interval = 50;
	poll_dev->poll = techjoy_poll;
	poll_dev->private = p;

	p->poll_dev = poll_dev;
	platform_set_drvdata(pdev, p);

	input = poll_dev->input;
	input->name = pdev->name;
	sprintf(p->phys, "techjoy/%s", input->dev.kobj.name);
	input->phys = p->phys;
	input->id.bustype = BUS_HOST;

	__set_bit(EV_KEY, input->evbit);
	__set_bit(BTN_A, input->keybit);
	__set_bit(BTN_B, input->keybit);
	__set_bit(EV_ABS, input->evbit);
	/* Hardcode min/max to the resolution of the 10-bit accelerometer w/ 2g scaling */
	input_set_abs_params(input, ABS_X, -255, 256, 0, 0);
	input_set_abs_params(input, ABS_Y, -255, 256, 0, 0);

	ret = input_register_polled_device(poll_dev);
	if (ret) {
		dev_err(dev, "unable to register input device: %d\n", ret);
		return ret;
	};

	return 0;
}

static int techjoy_remove(struct platform_device *pdev)
{
	struct techjoy *p = platform_get_drvdata(pdev);

	input_unregister_polled_device(p->poll_dev);

	return 0;
}

#ifdef CONFIG_OF
static const struct of_device_id techjoy_of_match[] = {
	{ .compatible = "bborg,techjoy", },
	{ }
};
MODULE_DEVICE_TABLE(of, techjoy_of_match);
#endif

static struct platform_driver __refdata techjoy_driver = {
	.driver = {
		.name = "techjoy",
		.of_match_table = of_match_ptr(techjoy_of_match),
	},
	.probe = techjoy_probe,
	.remove = techjoy_remove,
};
module_platform_driver(techjoy_driver);

MODULE_AUTHOR("Matt Porter");
MODULE_DESCRIPTION("Techlab cape joystick input driver");
MODULE_LICENSE("GPL v2");
