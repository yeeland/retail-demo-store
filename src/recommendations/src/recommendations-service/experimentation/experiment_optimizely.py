from . import experiment, resolvers
from optimizely import optimizely

# TODO: Ask James how we want the recommendations service to store the SDK Key
optimizely_sdk = optimizely.Optimizely(sdk_key='SDK_KEY')


class OptimizelyFeatureTest(experiment.Experiment):
    def get_items(self, user_id, current_item_id = None, item_list = None, num_results = 10, tracker = None):
        assert user_id, "`user_id` is required"

        # All the kwargs that are passed to ResolverFactory.get will be stored as a JSON feature variable.
        optimizely_sdk.is_feature_enabled(self.feature, user_id) # This sends an impression event
        resolver_init_kwargs = optimizely_sdk.get_feature_variable_json(self.feature, 'resolver_init_kwargs',
                                                                        user_id=user_id)
        resolver = resolvers.ResolverFactory.get(**resolver_init_kwargs)

        items = resolver.get_items(user_id=user_id,
                                   product_id=current_item_id,
                                   product_list=item_list,
                                   num_results=num_results)

        # TODO: Need to track impression events.
        return items
