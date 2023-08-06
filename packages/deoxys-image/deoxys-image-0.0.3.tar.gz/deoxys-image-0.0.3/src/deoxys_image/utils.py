import os


NUM_CPUS = None


def get_num_cpus():
    global NUM_CPUS
    if NUM_CPUS is None:
        try:
            NUM_CPUS = int(os.environ.get('NUM_CPUS'))
            if NUM_CPUS > 1:
                import ray
                if not ray.is_initialized():
                    ray.init(include_dashboard=False,
                             _temp_dir=os.environ.get('RAY_ROOT')
                             )
                    print(f'Initialized ray on {NUM_CPUS} cpus')
        except Exception as e:
            NUM_CPUS = 1
            print(e, 'Running augmentation on single processors')

    return NUM_CPUS
