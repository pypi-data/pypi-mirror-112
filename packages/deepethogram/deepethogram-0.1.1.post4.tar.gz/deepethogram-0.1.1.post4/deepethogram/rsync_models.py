import argparse
import os
import subprocess

remote_base = '/run/user/1000/gvfs/smb-share:server=research.files.med.harvard.edu,share=neurobio/HarveyLab/Tier1/Jim/DATA/deepethogram_revisions'
local_base = '/mnt/VIDEOS2'

projects = ['bohacek_EPM', 
            'bohacek_FST', 
            'bohacek_OFT', 
            'flies_revision', 
            'kc_yd_homecage', 
            'kc_yd_social', 
            'niv_revision', 
            'open_field_revision', 
            'woolf_revision']

def rsync(src, dst, exclude_pngs = True):
    assert os.path.isdir(src)
    assert os.path.isdir(dst)
    command = ['rsync',
               '-vha',
               '--no-perms',
               src,
               dst, 
               '--exclude', '*.zip']
    if exclude_pngs:
        command += ['--exclude', '*.png']
    print(' '.join(command))
    subprocess.run(command, check=True)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sync remote and local')
    parser.add_argument('-p', '--project', required=True, type=str,
                        help='which project')
    parser.add_argument('-d', '--direction', required=True, type=str, choices=['server_to_local', 'local_to_server'],
                        help='which direction to sync')
    parser.add_argument('--model_only', default=False, action='store_true', 
                        help='if true, only sync models folder')
    args = parser.parse_args()
    
    assert args.project in projects or args.project == 'all'
    
    project_list = projects if args.project == 'all' else [args.project]
    
    for project in project_list:
        remote_dir = os.path.join(remote_base, project + '_deepethogram')
        local_dir = os.path.join(local_base, project + '_deepethogram')
        
        if args.model_only:
            remote_dir = os.path.join(remote_dir, 'models')
            local_dir = os.path.join(local_dir, 'models')
            exclude_pngs = False
        else:
            exclude_pngs = True
        
        assert os.path.isdir(remote_dir)
        assert os.path.isdir(local_dir)
        
        if args.direction == 'server_to_local':
            src = remote_dir
            # for copying whole directories, dst should be the parent
            dst = os.path.dirname(local_dir)
            rsync(src, dst, exclude_pngs)
        else:
            src = local_dir
            dst = os.path.dirname(remote_dir)
            rsync(src, dst, exclude_pngs)
    