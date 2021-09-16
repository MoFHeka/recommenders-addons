# Copyright 2020 The TensorFlow Recommenders-Addons Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# lint-as: python3

from abc import ABCMeta
from tensorflow_recommenders_addons import dynamic_embedding as de


class KVCreator(object, metaclass=ABCMeta):
  """
      A generic KV table creator.

      KV table instance will be created by the create function with config.
    And also a config class for specific table instance backend should be
    inited before callling the creator function.
      And then, the KVCreator class instance will be passed to the Variable
    class for creating the real KV table backend(TF resource).

    Example usage:

    ```python
    redis_config1=tfra.dynamic_embedding.RedisTableConfig(
      redis_config_abs_dir="xx/yy.json"
    )
    redis_creator1=tfra.dynamic_embedding.RedisTableCreator(redis_config1)
    ```
  """

  def __init__(self, config=None):
    self.config = config

  def create(self,
             key_dtype=None,
             value_dtype=None,
             default_value=None,
             name=None,
             checkpoint=None,
             init_size=None,
             config=None):

    raise NotImplementedError('create function must be implemented')


class CuckooHashTableConfig(object):

  def __init__(self):
    """ CuckooHashTableConfig include nothing for parameter default satisfied.
    """
    pass


class CuckooHashTableCreator(KVCreator):

  def create(
      self,
      key_dtype=None,
      value_dtype=None,
      default_value=None,
      name=None,
      checkpoint=None,
      init_size=None,
      config=None,
  ):
    return de.CuckooHashTable(
        key_dtype=key_dtype,
        value_dtype=value_dtype,
        default_value=default_value,
        name=name,
        checkpoint=checkpoint,
        init_size=init_size,
        config=config,
    )


class RedisTableConfig(object):
  """ 
      RedisTableConfig config json file for connecting Redis service and 
    assign the embedding table starage properties.
      An example of a configuration file is shown below:
      ""
      {
        "redis_connection_mode": 1,
        "redis_master_name": "master",
        "redis_host_ip": [
          "127.0.0.1"
        ],
        "redis_host_port": 6379,
        "redis_user": "default",
        "redis_password": "",
        "redis_db": 0,
        "redis_connect_keep_alive": False,
        "redis_connect_timeout": 1000,
        "redis_socket_timeout": 1000,
        "redis_conn_pool_size": 20,
        "redis_wait_timeout": 100000000,
        "redis_connection_lifetime": 100,
        "redis_sentinel_connect_timeout": 1000,
        "redis_sentinel_socket_timeout": 1000,
        "storage_slice": 1,
        "keys_sending_size": 1024,
        "using_md5_prefix_name": False,
        "model_tag_import": "test",
        "redis_hash_tags_import": [],
        "model_tag_runtime": "test",
        "redis_hash_tags_runtime": [],
        "expire_model_tag_in_seconds": 604800,
        "table_store_mode": 1,
        "model_lib_abs_dir": "/tmp/"
      }
      ""
      Refer to the default_redis_params variable in RedisTable class 
    for the description of the JSON configuration file
  """

  def __init__(
      self,
      redis_config_abs_dir="/tmp/redis_config.json",
  ):
    self.redis_config_abs_dir = redis_config_abs_dir


class RedisTableCreator(KVCreator):
  """ 
      RedisTableCreator will create a object to pass itself to the others classes
    for creating a real Redis client instance which can interact with TF.
  """

  def create(
      self,
      key_dtype=None,
      value_dtype=None,
      default_value=None,
      name=None,
      checkpoint=None,
      init_size=None,
      config=None,
  ):
    real_config = config if config is not None else self.config
    if not isinstance(real_config, RedisTableConfig):
      raise TypeError("config should be instance of 'config', but got ",
                      str(type(real_config)))
    return de.RedisTable(
        key_dtype=key_dtype,
        value_dtype=value_dtype,
        default_value=default_value,
        name=name,
        checkpoint=checkpoint,
        config=self.config,
    )