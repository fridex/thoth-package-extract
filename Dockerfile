FROM fedora:28

ENV PATH=$HOME/.local/bin/:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    GOPATH='/tmp/go'

LABEL io.k8s.description="Thoth Package Extract Base" \
    io.k8s.display-name="Thoth: Package Extract Base" \
    io.openshift.tags="thoth,python,go,mercator,package-extract" \
    architecture=x86_64 \
    vendor="Red Hat Office of the CTO - AI CoE" \
    license="GPLv3"

RUN dnf update -y && \
    dnf install -y python-pip go git make skopeo dnf-utils fakeroot fakechroot && \
    dnf clean all

COPY ./ /tmp/package-extract
RUN cd /tmp/package-extract && \
    make all && \
    rm -rf /tmp/package-extract

USER 1042
CMD ["extract-image"]
ENTRYPOINT ["thoth-package-extract"]

