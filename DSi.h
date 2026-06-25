#ifndef DSI_HEADERS_H
#define DSI_HEADERS_H

// ---------------------------------------------
// Enum of all known DSi HTTP headers
// ---------------------------------------------
typedef enum {
    DSI_HDR_MAC,
    DSI_HDR_ID,
    DSI_HDR_SID,
    DSI_HDR_AUTH_RESPONSE,
    DSI_HDR_REGION,
    DSI_HDR_LANG,
    DSI_HDR_COUNTRY,
    DSI_HDR_USER_NAME,
    DSI_HDR_BIRTHDAY,
    DSI_HDR_DATETIME,
    DSI_HDR_COLOR,
    DSI_HDR_UGOMEMO_VERSION,
    DSI_HDR_UNKNOWN
} DSiHeaderType;


// ---------------------------------------------
// Struct for mapping header strings to enum
// ---------------------------------------------
typedef struct {
    const char* name;
    DSiHeaderType type;
} DSiHeaderEntry;


// ---------------------------------------------
// Lookup table of all X‑DSi‑ headers
// ---------------------------------------------
static const DSiHeaderEntry DSI_HEADER_TABLE[] = {

    { "X-DSi-MAC",          DSI_HDR_MAC },
    { "X-DSi-ID",           DSI_HDR_ID },
    { "X-DSi-SID",          DSI_HDR_SID },
    { "X-DSi-Auth-Response",DSI_HDR_AUTH_RESPONSE },

    { "X-DSi-Region",       DSI_HDR_REGION },
    { "X-DSi-Lang",         DSI_HDR_LANG },
    { "X-DSi-Country",      DSI_HDR_COUNTRY },

    { "X-DSi-User-Name",    DSI_HDR_USER_NAME },
    { "X-Birthday",         DSI_HDR_BIRTHDAY },
    { "X-DSi-DateTime",     DSI_HDR_DATETIME },
    { "X-DSi-Color",        DSI_HDR_COLOR },

    { "X-Ugomemo-Version",  DSI_HDR_UGOMEMO_VERSION },

    { NULL,                 DSI_HDR_UNKNOWN }
};


// ---------------------------------------------
// Helper: Convert header string → enum
// ---------------------------------------------
static inline DSiHeaderType dsi_get_header_type(const char* header) {
    for (int i = 0; DSI_HEADER_TABLE[i].name != NULL; i++) {
        if (strcmp(header, DSI_HEADER_TABLE[i].name) == 0)
            return DSI_HEADER_TABLE[i].type;
    }
    return DSI_HDR_UNKNOWN;
}

#endif
