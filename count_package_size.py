import argparse
import pathlib
import os

os.system("pip list | tail -n +3 | awk '{print $1}' | xargs pip show | grep -E 'Location:|Name:' | cut -d ' ' -f 2 | paste -d ' ' - - | awk '{print $2 \"/\" tolower($1)}' | xargs du -sh 2> /dev/null | sort -hr")
os.system("pip list | tail -n +3 | awk '{print $1}' | xargs pip show | grep -E 'Location:|Name:' | cut -d ' ' -f 2 | paste -d ' ' - - | awk '{print $2 \"/\" tolower($1)}' | xargs du -sh 2> /dev/null | sort -hr > package_sizes.txt")
os.system("sed -i '' 's@/.*@@' package_sizes.txt")

parser = argparse.ArgumentParser()
parser.add_argument('--input_file',
					type=pathlib.Path,
					default='package_sizes.txt')

args = parser.parse_args()

input_list = args.input_file.read_text().replace('\t', '').split('\n')
input_list = list(filter(lambda x: len(x) > 0, input_list))

running_mb_sum = 0

for size in input_list:

	if size.endswith('M'):
		running_mb_sum += float(size.strip('M'))

	elif size.endswith('K'):
		running_mb_sum += float(size.strip('K')) * 0.001

	else:
		raise Exception('Not Megabyte or Kilobyte size')


print(f'Sum of package sizes: {round(running_mb_sum, 2)}M')