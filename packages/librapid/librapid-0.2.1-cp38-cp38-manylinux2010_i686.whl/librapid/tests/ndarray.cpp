#include <iostream>
#include <chrono>

// #define LIBRAPID_CBLAS

#include "ndarray_benchmarks.hpp"
#include <librapid/ndarray/ndarray.hpp>

int main()
{
	std::cout << "Value: " << librapid::math::round(153, -2) << "\n";
	std::cout << "Value: " << librapid::math::round_sigfig(123.456, 4) << "\n";

	auto train_input = librapid::from_data(VEC<VEC<double>>{
			{0, 0},
			{0, 1},
			{1, 0},
			{1, 1}
	});

	auto train_output = librapid::from_data(VEC<VEC<double>>{
			{0},
			{1},
			{1},
			{0}
	});

	train_input.reshape({4, 2, 1});
	train_output.reshape({4, 1, 1});

	auto activation1 = new librapid::activations::sigmoid<double>();
	auto activation2 = new librapid::activations::sigmoid<double>();

	auto optimizer1 = new librapid::optimizers::sgd<double>(0.1);
	auto output_optimizer = new librapid::optimizers::sgd<double>(0.1);

	auto input_layer = new librapid::layers::input<double>(2);
	auto hidden_layer_1 = new librapid::layers::affine<double>(3, activation1, optimizer1);
	auto output_layer = new librapid::layers::affine<double>(1, activation2, output_optimizer);

	auto network = librapid::network<double>();
	network.add_layer(input_layer);
	network.add_layer(hidden_layer_1);
	network.add_layer(output_layer);

	network.compile();

	std::cout << "Inputs\n" << train_input << "\n\n";
	std::cout << "Outputs\n" << train_output << "\n\n";

	for (lr_int i = 0; i < 4; i++)
	{
		std::cout << "Input: " << train_input[i].str(7) << "\n";
		std::cout << "Output: " << network.forward(train_input[i]) << "\n\n\n";
	}

	std::cout << "\n\n\n";

	auto start = TIME;
	for (lr_int i = 0; i < 3000 * 4; i++)
	{
		lr_int index = librapid::math::random(0, 3);
		network.backpropagate(train_input[index], train_output[index]);
	}
	auto end = TIME;
	std::cout << "Time: " << end - start << "\n";

	for (lr_int i = 0; i < 4; i++)
	{
		std::cout << "Input: " << train_input[i].str(7) << "\n";
		std::cout << "Output: " << network.forward(train_input[i]) << "\n";
	}

	std::string space(10, ' ');

	std::cout << "/" << std::string(22, '=') << "\\";
	std::cout << space;
	std::cout << "/" << std::string(22, '=') << "\\\n";

	for (int y = 0; y < 20; y++)
	{
		std::cout << "||";
		for (int x = 0; x < 20; x++)
		{
			double x_coord = x / 20.;
			double y_coord = y / 20.;

			auto res = network.forward(librapid::ndarray::from_data(std::vector<double>{x_coord, y_coord}).reshaped({2, 1}));
			double val = res[0][0].to_scalar();

			//  . - * % & #
			if (val > 0.86)
				std::cout << "#";
			else if (val > 0.71)
				std::cout << "&";
			else if (val > 0.57)
				std::cout << "%";
			else if (val > 0.43)
				std::cout << "*";
			else if (val > 0.32)
				std::cout << "-";
			else if (val > 0.14)
				std::cout << ".";
			else
				std::cout << " ";
		}
		std::cout << "||";

		std::cout << space;

		std::cout << "||";
		for (int x = 0; x < 20; x++)
		{
			double x_coord = x / 20.;
			double y_coord = y / 20.;

			if (abs(x_coord - y_coord) > 0.5)
				std::cout << "#";
			else
				std::cout << " ";
		}
		std::cout << "||\n";
	}

	std::cout << "\\" << std::string(22, '=') << "/";
	std::cout << space;
	std::cout << "\\" << std::string(22, '=') << "/\n";

	return 0;
}