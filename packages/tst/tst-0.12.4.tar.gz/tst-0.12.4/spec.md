What does tst expect from a json web activity resource?

It should expect the very minimal.

- the `files` property is the only mandatory property
- the `dirname` property can be used to specify a directory name
  to use (the cli user can overwrite this, but if the user
  doesn't give the <dir> argument and `dirname` is available,
  `tst` will use it without confirmation)
- if `dirname` is not provided, `tst` will lookup properties
  `name`, `id` and `iid` as well, considering them as
  possible alternatives for a directory name; however, they will
  be confirmed with the cli user;

