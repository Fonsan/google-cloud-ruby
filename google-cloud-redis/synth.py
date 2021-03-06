import synthtool as s
import synthtool.gcp as gcp
import logging
import re


logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()

# Temporary until we get Ruby-specific tools into synthtool
def merge_gemspec(src, dest, path):
    regex = re.compile(r'^\s+gem.version\s*=\s*"[\d\.]+"$', flags=re.MULTILINE)
    match = regex.search(dest)
    if match:
        src = regex.sub(match.group(0), src, count=1)
    regex = re.compile(r'^\s+gem.homepage\s*=\s*"[^"]+"$', flags=re.MULTILINE)
    match = regex.search(dest)
    if match:
        src = regex.sub(match.group(0), src, count=1)
    return src

v1beta1_library = gapic.ruby_library(
    'redis', 'v1beta1',
    config_path='artman_redis_v1beta1.yaml',
    artman_output_name='google-cloud-ruby/google-cloud-redis'
)
s.copy(v1beta1_library / 'lib')
s.copy(v1beta1_library / 'test')
s.copy(v1beta1_library / 'Rakefile')
s.copy(v1beta1_library / 'README.md')
s.copy(v1beta1_library / 'LICENSE')
s.copy(v1beta1_library / '.gitignore')
s.copy(v1beta1_library / '.rubocop.yml')
s.copy(v1beta1_library / '.yardopts')
s.copy(v1beta1_library / 'google-cloud-redis.gemspec', merge=merge_gemspec)

# https://github.com/googleapis/gapic-generator/issues/2196
s.replace(
    [
      'README.md',
      'lib/google/cloud/redis.rb',
      'lib/google/cloud/redis/v1beta1.rb',
      'lib/google/cloud/redis/v1beta1/doc/overview.rb'
    ],
    '\\[Product Documentation\\]: https://cloud\\.google\\.com/redis\n',
    '[Product Documentation]: https://cloud.google.com/memorystore\n')

# https://github.com/googleapis/gapic-generator/issues/2232
s.replace(
    'lib/google/cloud/redis/v1beta1/cloud_redis_client.rb',
    '\n\n(\\s+)class OperationsClient < Google::Longrunning::OperationsClient',
    '\n\n\\1# @private\n\\1class OperationsClient < Google::Longrunning::OperationsClient')
