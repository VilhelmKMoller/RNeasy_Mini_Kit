from opentrons import protocol_api
import math
"""
Make pippetting protocol using tecan with Quigan kit: RNeasy mini kit 
Used for purification of RNA.

Version 1
owner: Vilhelm 
date: 2021.01.13

URL for kit: https://www.qiagen.com/gb/shop/automated-solutions/sample-disruption/rneasy-mini-kit/
"""


## 1. metadata
metadata = {
    'protocolName': 'RNA purification',
    'author': 'Name <vikmol@biosustain.dtu.dk>',
    'description': 'RNA purification using Quigan RNesy mini kit',
    'apiLevel': '2.8'
}

## 2. protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    ## 3. labware
    # labware names: https://labware.opentrons.com/
	reservoir = protocol.load_labware('nest_12_reservoir_15ml', '10')
	sample_plate = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', '11')
	reagents_plate = protocol.load_labware('opentrons_24_aluminumblock_generic_2ml_screwcap', '9') 
    # tips
	tip_rack_1 = protocol.load_labware('opentrons_96_filtertiprack_20ul', '2')
	tiprack_1000_1 = protocol.load_labware('geb_96_tiprack_1000ul', '1')

    ## 4. pipettes
	pipette_p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tip_rack_1])
	pipette_p1000 = protocol.load_instrument('p1000_single', 'left', tip_racks=[tiprack_1000_1])

   
    ################################ CHANGE THIS NUMBER TO FIT NUMBER OF SAMPLES ##########
    # max number of samples 12
	number_of_samples = 2 
	## OPS make an error command if number_of_samples < 12
	################################3######################################################

	## 5. commands  

    # get SUPER-IN and aspirate it into sample
	for n in range(number_of_samples):
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(1, reagents_plate['A3']) # Aspirate 1uL from reagents_plate positon[A1]

		# start in C1-6
		if n <= 5:
			pipette_p20.dispense(1, sample_plate.rows()[2][n])
		# go to D1-6
		elif n >= 6:
			pipette_p20.dispense(1, sample_plate.rows()[3][n-6])
		# mix 3 times, 20uL, in current location
		pipette_p20.mix(3, 20)
		pipette_p20.drop_tip()

	
	# Lysozyme to Master Mix 1
	ul_amount = (number_of_samples+1)*3
	# ul_amount MUST BE <20ul. Will work if less than 12 samples are run:
	if ul_amount > 20:
		ul_amount_half = ul_amount / 2
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount_half, reagents_plate['A1'])
		pipette_p20.dispense(ul_amount_half, sample_plate['A3'])
		pipette_p20.drop_tip()

		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount_half, reagents_plate['A1'])
		pipette_p20.dispense(ul_amount_half, sample_plate['A3'])
		pipette_p20.drop_tip()
	else:
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount, reagents_plate['A1'])
		pipette_p20.dispense(ul_amount, sample_plate['A3'])
		pipette_p20.drop_tip()


	# Proteinase K to Master Mix 1
	ul_amount = number_of_samples+1
	# ul_amount MUST BE <20ul
	if ul_amount > 20:
		ul_amount_half = ul_amount / 2
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount_half, reagents_plate['B1'])
		pipette_p20.dispense(ul_amount_half, sample_plate['A3'])
		pipette_p20.drop_tip()

		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount_half, reagents_plate['B1'])
		pipette_p20.dispense(ul_amount_half, sample_plate['A3'])
		pipette_p20.drop_tip()
	else:
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount, reagents_plate['B1'])
		pipette_p20.dispense(ul_amount, sample_plate['A3'])
		pipette_p20.drop_tip()


	# SDS added to Master Mix 1
	ul_amount = (number_of_samples+1)*3
	# ul_amount MUST BE <20ul
	if ul_amount > 20:
		ul_amount_half = ul_amount / 2
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount_half, sample_plate['A1'])
		pipette_p20.dispense(ul_amount_half, sample_plate['A3'])
		pipette_p20.drop_tip()

		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount_half, sample_plate['A1'])
		pipette_p20.dispense(ul_amount_half, sample_plate['A3'])
		pipette_p20.mix(3, 20)
		pipette_p20.drop_tip()
	else:
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount, sample_plate['A1'])
		pipette_p20.dispense(ul_amount, sample_plate['A3'])
		pipette_p20.mix(3, 20)
		pipette_p20.drop_tip()


	# Add MM1 to sample 
	for n in range(number_of_samples):
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(7, sample_plate['A3'])
		# samples C1-6
		if n <= 5:
			pipette_p20.dispense(7, sample_plate.rows()[2][n])
		# go to D1-6
		elif n >= 6:
			pipette_p20.dispense(7, sample_plate.rows()[3][n-6])		
		pipette_p20.mix(10, 20)
		pipette_p20.drop_tip()


	# pause for 20 minutes - the time it take for each sample to be mixed with Master mix 1(1min)
	# subtract the time it takes to make Master mix 2(2min)
	protocol.delay(minutes=(20-number_of_samples-2)) 


	## Add DNAse I to Master mix 2
	ul_amount = (number_of_samples+1)*5
	# ul_amount MUST BE <20ul
	if ul_amount > 20:
		rounds = math.ceil(ul_amount / 20)
		aliquote = ul_amount / rounds
		for n in range(rounds):
			pipette_p20.pick_up_tip()
			pipette_p20.aspirate(aliquote, reagents_plate['A5'])
			pipette_p20.dispense(aliquote, reagents_plate['D5'])
			pipette_p20.drop_tip()
	else:
		pipette_p20.pick_up_tip()
		pipette_p20.aspirate(ul_amount, reagents_plate['A5'])
		pipette_p20.dispense(ul_amount, reagents_plate['D5'])
		pipette_p20.drop_tip()


	## Add RDD buffer to Master mix 2
	# ul_amount MUST BE <1000ul
	ul_amount = (number_of_samples+1)*20
	pipette_p1000.pick_up_tip()
	pipette_p1000.aspirate(ul_amount, reservoir['A1'])
	pipette_p1000.dispense(ul_amount, reagents_plate['D5'])
	pipette_p1000.mix(5, 25)
	pipette_p1000.drop_tip()


	# add MM2 to sample
	for n in range(number_of_samples):
		pipette_p1000.pick_up_tip()
		pipette_p1000.aspirate(25, reagents_plate['D5']) #mistake was set to sample_plate['D5']

		# samples C1-6
		if n <= 5:
			pipette_p1000.dispense(25, sample_plate.rows()[2][n])
		# go to D1-6
		elif n >= 6:
			pipette_p1000.dispense(25, sample_plate.rows()[3][n-6])

		pipette_p1000.mix(2, 25)
		pipette_p1000.drop_tip()


	# add RLT buffer to sample
	for n in range(number_of_samples):
		pipette_p1000.pick_up_tip()
		pipette_p1000.aspirate(700, reservoir['A3'])

		# samples C1-6
		if n <= 5:
			pipette_p1000.dispense(700, sample_plate.rows()[2][n])
		# go to D1-6
		elif n >= 6:
			pipette_p1000.dispense(700, sample_plate.rows()[3][n-6])

		pipette_p1000.mix(5, 800)
		pipette_p1000.drop_tip()


	# add EtOH buffer to sample
	for n in range(number_of_samples):
		pipette_p1000.pick_up_tip()
		pipette_p1000.aspirate(500, reservoir['A5'])

		# samples C1-6
		if n <= 5:
			pipette_p1000.dispense(500, sample_plate.rows()[2][n])
		# go to D1-6
		elif n >= 6:
			pipette_p1000.dispense(500, sample_plate.rows()[3][n-6])

		pipette_p1000.mix(5, 800)
		pipette_p1000.drop_tip()
		


