# vqktrCS`s MCBE Compiler and Workspace Generator
A simple Python-based compiler that moves Resource Pack (RP) and Behavior Pack (BP) folders into Minecraft Bedrock’s development directories - perfect for bypassing Windows or Microsoft file-editing restrictions.

# Why the compiler?
Some Windows systems restrict moving files to certain drives that are locked by Windows. Often times you see this message "The organisation does not allow you to place this file here" error message. Which is frustrating for people who edit their Addons under certain conditions. 

See this post: https://www.reddit.com/r/WindowsHelp/comments/1ezi870/the_organisation_does_not_allow_you_to_place_this

# How to use?
Run this command: 
`git clone https://github.com/vqktrCS/mcbe_compiler`

Edit the `create_workspace.bat` if you intend to change the command line args for the `generate_workspace.py` file. 

Run the batch file `create_workspace.bat` to create your workspace

or you can manually run this command:
`py generate_workspace.py --name "Your Pack name" --desc "Your Pack description"`

# How do I compile my mod?
You can compile the mod by running this command on a terminal:
`py compiler.py`

or run the `compile.workspace.bat` file to compile your addon without having to type the python command.

# Compiling the mod
You have options to set a custom path which is good for test directories outside your main addon workspace.
You also have the option to wipe the `development_resource_packs` and `development_behavior_packs` directory if you want a clean installation of your addon. Note that you should probably move out any pre-existing addons inside the directory to avoid accidental file overrides or deletion.

The compiler should automatically put your `BP` and `RP` folders in Minecraft`s development directories.

Happy Modding Bedrock Community!
