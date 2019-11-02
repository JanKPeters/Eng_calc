# -*- coding: utf-8 -*-

import heattransfer
import pandas as pd
import plotnine as p9

# air_velocity_inside = float(input("Air velocity inside in m/s: "))
# air_velocity_outside = float(input("Air velocity outside in m/s: "))
# t_inside = float(input("Max. expected gas temperature inside in °C: "))
# t_outside = float(input("Expected gas temperature outside in °C: "))
# surface = float(input("Surface area to be calculated in m²: "))
# layers =  int(input("How many layers make up the wall?: "))
# wall_thickness = [0.19,0.07,0.03]
# thermal_conductivity = [1.5,0.89,45]

# for i in range(layers):
#     layer_thickness = float(input(f"How thick is layer {i + 1} in meters?: "))
#     wall_thickness.append(layer_thickness)
#     layer_conductivity = float(input(f"What is the layer {i + 1} conductivity in W/m/k?: "))
#     thermal_conductivity.append(layer_conductivity)

def htcalc (air_velocity_inside, air_velocity_outside, t_inside, t_outside, surface, layers, wall_thickness, thermal_conductivity):
    # We need the convective heat resistance on both sides of the wall
    res_conv_inside = heattransfer.convective_resistance(heattransfer.heat_transfer_coef(air_velocity_inside), surface)
    res_conv_outside = heattransfer.convective_resistance(heattransfer.heat_transfer_coef(air_velocity_outside), surface)

    # We need the total resistance over all wall layers
    total_layer_resistance = []
    total_layer_resistance.append(res_conv_inside)
    for i in range (layers):
        total_layer_resistance.append(heattransfer.conductive_resistance(wall_thickness[i], thermal_conductivity[i], surface))

    total_layer_resistance.append(res_conv_outside)

    total_resistance = sum(total_layer_resistance)

    heat_transfer = heattransfer.conduction(t_inside, t_outside, total_resistance)

    # Calculating the temperatures between each layer
    temperatures = []
    temperatures.append(t_inside)
    layer_resistance = 0
    for resistance in total_layer_resistance:
        layer_resistance += resistance
        temperatures.append(heattransfer.layer_temperature(heat_transfer, layer_resistance, t_inside))

    # Preparing the x axis, position of the temperature and transition labels for the graph
    position = [0, 0.02]
    labels = ['gas inside', 'inner surface']

    i = 0
    for entry in wall_thickness:
        position.append(position[-1] + entry)
        i += 1
        labels.append("layer" + str(i))

    labels[-1] = "outer surface"
    position.append(position [-1] + 0.02)
    labels.append("gas outside")

    # print(f"\nThe total resistance is {round(total_resistance, 2)} K/W")
    # print(f"Total heat transfer from inside to outside is {round(heat_transfer, 2)} W\n")
    # for temp in temperatures:
    #     if temperatures.index(temp) == 0:
    #         print(f"-- gas temperature -- {round(temp, 2)}°C --")
    #         print(f"-- oooooooooooooooooooooooooooooooooooo --")
    #     elif temperatures.index(temp) == 1:
    #         print(f"-- inner surface -- {round(temp, 2)}°C --")
    #         print(f"-- |||||||||| wall layer |||||||||||||| --")
    #     elif temperatures.index(temp) == len(temperatures) - 2:
    #         print(f"-- outer surface -- {round(temp, 2)}°C --")
    #         print(f"-- oooooooooooooooooooooooooooooooooooo --")
    #     elif temperatures.index(temp) == len(temperatures) - 1:
    #         print(f"-- gas temperature -- {round(temp, 2)}°C --")
    #     else:
    #         print(f"-- layer surface -- {round(temp, 2)}°C --")
    #         print(f"-- |||||||||| wall layer |||||||||||||| --")

    df = pd.DataFrame(
        {'pos': position,
        'temp': temperatures
        })

    gg = p9.ggplot(df, p9.aes(x='pos', y='temp'))
    gg += p9.geom_line(p9.aes(color='temp'), size=2)

    for ws in df.pos.values.tolist():
        gg += p9.geom_vline(xintercept=ws, color='grey')

    gg += p9.geom_hline(yintercept=110, color='red', size=2, alpha=0.8)
    gg += p9.ggtitle('heat transfer through wall')
    gg += p9.scale_x_continuous(name='Position', breaks=df.pos.values.tolist(), labels=labels)
    gg += p9.scale_y_continuous(name='Temperature', breaks=range(0,800,50), limits=(0,800))
    gg += p9.theme(axis_text_x=p9.element_text(angle = 45))
    gg += p9.scale_colour_gradient(low = "yellow", high = "orange")

    i = 0
    for temp in temperatures:
        gg += p9.geom_text(p9.aes(x = position[i], y = temp+30, label = round(temp, 2)))
        i += 1

    labtext = 'Thermal cond.: ' + str(thermal_conductivity[0]) + '[W/m/K]\nLayer thickness: ' + str(round(wall_thickness[0], 3)) + '[m]'
    gg += p9.annotate(geom='text', x = ((position[2]-position[1])/2)+position[1], y = temperatures[0]+30, 
                      label = labtext, color='blue')

    return gg
    # gg.draw()
