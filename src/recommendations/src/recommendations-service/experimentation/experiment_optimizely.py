import os

from optimizely import optimizely

from . import experiment, resolvers


optimizely_sdk = optimizely.Optimizely(sdk_key=os.environ('OPTIMIZELY_SDK_KEY'))


class OptimizelyFeatureTest(experiment.Experiment):
    def get_items(self, user_id, current_item_id = None, item_list = None, num_results = 10, tracker = None):
        assert user_id, "`user_id` is required"

        # All the kwargs that are passed to ResolverFactory.get will be stored as a JSON feature variable.
        resolver_init_kwargs = optimizely_sdk.get_feature_variable_json(self.feature, 'resolver_init_kwargs',
                                                                        user_id=user_id)
        resolver = resolvers.ResolverFactory.get(**resolver_init_kwargs)

        items = resolver.get_items(user_id=user_id,
                                   product_id=current_item_id,
                                   product_list=item_list,
                                   num_results=num_results)

        config = optimizely_sdk.config_manager.get_config()

        for item in items:
            item['experiment'] = {'type': 'optimizely',
                                  'feature': self.feature,
                                  'revision_number': config.get_revision()}
        return items
