require 'rubygems'

CODE = '5678901234'

# Substitute for %CODE%
template_split_begin = template.index(CODE)
template_split_end = template_split_begin + 6

template_part_one =
String.new(template[0..(template_split_begin-1)])

template_part_two =
String.new(template[template_split_end..template.length])

code = String.new(req_id)

template =
String.new(template_part_one + code + template_part_two)

puts template
