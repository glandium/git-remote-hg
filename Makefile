PYTHON_SCRIPTS := \
	git-remote-hg.py \
	git-cinnabar.py \

PYTHON_LIBS := \
	githg/__init__.py \
	githg/bundle.py \
	githg/dag.py \
	git/__init__.py \
	git/util.py

ifneq (,$(wildcard $(CURDIR)/git-core/Makefile))
all:

.SUFFIXES:

%:
	$(MAKE) -C $(CURDIR)/git-core -f $(CURDIR)/Makefile $@ SCRIPT_PYTHON="git-p4.py $(PYTHON_SCRIPTS)"

else

include $(CURDIR)/Makefile

VPATH += ..

all:: $(addprefix pythonlib/,$(PYTHON_LIBS))

$(addprefix pythonlib/,$(PYTHON_LIBS)): pythonlib/%: %
	$(INSTALL) -d ${@D}
	$(INSTALL) -m 644 $^ $@

install: install-pythonlib
clean: clean-pythonlib

PYTHON_LIBS_DIRS := $(sort $(dir $(PYTHON_LIBS)))

define _
$1

endef

.PHONY: install-pythonlib clean-pythonlib
install-pythonlib:
	$(foreach dir,$(PYTHON_LIBS_DIRS),$(call _,$(INSTALL) -d -m 755 '$(DESTDIR_SQ)$(gitexec_instdir_SQ)/pythonlib/$(dir)'))
	$(foreach dir,$(PYTHON_LIBS_DIRS),$(call _,$(INSTALL) -m 644 $(addprefix pythonlib/,$(filter $(dir)%,$(PYTHON_LIBS))) '$(DESTDIR_SQ)$(gitexec_instdir_SQ)/pythonlib/$(dir)'))

clean-pythonlib:
	$(RM) -r pythonlib
endif
