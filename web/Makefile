LIBS_TO_BUILD=chatroom tunneling
LIBS_TO_BUILD_RULES=$(addprefix build-,${LIBS_TO_BUILD})

APPS_TO_BUILD=chatroom  
APPS_TO_BUILD_RULES=$(addprefix build-,${APPS_TO_BUILD})

check:
	pnpx gts check
	pnpx prettier --check **/*.html

fix:
	pnpx gts fix
	pnpx prettier **/*.html --write

build: $(LIBS_TO_BUILD_RULES)

build-apps: cleanup-public $(APPS_TO_BUILD_RULES)

cleanup-public:
	rm -rf public
	mkdir -p public

#setup-development-environment:
#	npm install -g pnpm@7.1.6
#	pnpm install

$(LIBS_TO_BUILD_RULES): build-%: libs/%
	pnpm --prefix $< build

$(APPS_TO_BUILD_RULES): build-%: apps/%
	pnpm --prefix $< install
	pnpm --prefix $< build
	mv $</dist public/$(<F)
