import os
import click

from ds_plugin.proto import model_pb2, schema_pb2

# @click.command()
# @click.option('--converted_model', type=str)
# @click.option('--validate_samples', type=str, default='')
# @click.option('--output', type=str)
# @click.option('--model_name', type=str)
# @click.option('--namespace', type=str)
# @click.option('--target', type=str, default='sg')
# @click.option('--local_emb', type=bool, default=True)
# @click.option('--validate_accuracy', type=int, default=5)
# @click.option('--validate_rate', type=int, default=99)
# @click.option('--cyclone_wait_timeout', type=int, default=3600)
# def main(
#         converted_model,
#         validate_samples,
#         output,
#         model_name,
#         namespace,
#         target,
#         local_emb,
#         validate_accuracy,
#         validate_rate,
#         cyclone_wait_timeout
#     ):
#     print ("converted_model: %s" % converted_model)
#     print ("validate_samples: %s" % validate_samples)
#     print ("output: %s" % output)
#     print ("model_name: %s" % model_name)
#     print ("namespace: %s" % namespace)
#     print ("target: %s" % target)
#     print ("local_emb: %s" % local_emb)
#     print ("validate_accuracy: %s" % validate_accuracy)
#     print ("validate_rate: %s" % validate_rate)
#     print ("cyclone_wait_timeout: %s" % cyclone_wait_timeout)

@click.command()
@click.option('--target', type=str, default='sg')
def main(target):
    print ("target: %s" % target)


if __name__ == '__main__':
    main()