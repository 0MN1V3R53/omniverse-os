import re

file_path = '/Users/silversurfer/Documents/Omniverse2/sky_next/components/QuoteCalculator.jsx'
with open(file_path, 'r') as f:
    content = f.read()

# 1. Increment generic text classes
content = content.replace('text-5xl', 'TEMP_5XL')
content = content.replace('text-2xl', 'TEMP_2XL')
content = content.replace('text-lg', 'TEMP_LG')
content = content.replace('text-base', 'TEMP_BASE')
content = content.replace('text-sm', 'TEMP_SM')
content = content.replace('text-xs', 'TEMP_XS')

content = content.replace('TEMP_5XL', 'text-6xl')
content = content.replace('TEMP_2XL', 'text-3xl')
content = content.replace('TEMP_LG', 'text-xl')
content = content.replace('TEMP_BASE', 'text-lg')
content = content.replace('TEMP_SM', 'text-base')
content = content.replace('TEMP_XS', 'text-sm')

# 2. Add text-lg to inputs
content = content.replace(
    'const clsBase = "w-full bg-black/50 border border-gray-300/30 rounded-lg px-4 py-3 text-white placeholder-gray-500',
    'const clsBase = "w-full bg-black/50 border border-gray-300/30 rounded-lg px-4 py-3 text-white text-lg placeholder-gray-500'
)
content = content.replace(
    'const clsErr = "w-full bg-black/50 border border-red-500 rounded-lg px-4 py-3 text-white placeholder-gray-500',
    'const clsErr = "w-full bg-black/50 border border-red-500 rounded-lg px-4 py-3 text-white text-lg placeholder-gray-500'
)

# 3. Center headings
content = content.replace(
    '<h3 className="text-3xl font-bold mb-2">Instant Quote Calculator</h3>',
    '<h3 className="text-4xl font-bold mb-2 text-center">Instant Quote Calculator</h3>' # It became 3xl in step 1, I'll make it 4xl just to be sure it's big!
)
content = content.replace(
    '<p className="text-gray-400 text-base">Step {step} of 4</p>',
    '<p className="text-gray-400 text-lg text-center">Step {step} of 4</p>'
)

content = content.replace(
    '<h4 className="text-xl font-bold text-white mb-1">Your Instant Price Estimate</h4>',
    '<h4 className="text-3xl font-bold text-white mb-1 text-center">Your Instant Price Estimate</h4>'
)
content = content.replace(
    '<h4 className="text-xl font-bold text-white mb-2">Your Quote is Ready!</h4>',
    '<h4 className="text-3xl font-bold text-white mb-2 text-center">Your Quote is Ready!</h4>'
)
content = content.replace(
    '<h4 className="text-xl font-bold text-white">Contact Information <span className="text-rose-400 text-base font-normal">(All fields required)</span></h4>',
    '<h4 className="text-3xl font-bold text-white text-center">Contact Information <span className="block text-rose-400 text-base font-normal mt-1">(All fields required)</span></h4>'
)


with open(file_path, 'w') as f:
    f.write(content)

print("Text sizes increased and headings centered.")
